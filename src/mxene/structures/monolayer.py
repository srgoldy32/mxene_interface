# src/mxene/structures/monolayer.py
import atomman as am
import numpy as np
from .unit import get_possible_vacancies
from mxene.io.paths import UNITS_DIR


def _parse_supercell_size(size: str) -> tuple[int, int]:
    try:
        dupx_str, dupy_str = size.lower().split('x', maxsplit=1)
        dupx = int(dupx_str)
        dupy = int(dupy_str)
    except (ValueError, AttributeError) as exc:
        raise ValueError("size must be in '<int>x<int>' format, e.g. '4x4'") from exc

    if dupx < 1 or dupy < 1:
        raise ValueError('size values must both be >= 1')

    return dupx, dupy


def _parse_vacancy_condition(vacancy_condition: str) -> tuple[str, int | None]:
    vacancy_condition = vacancy_condition.strip().lower()
    if vacancy_condition == 'pris':
        return vacancy_condition, None

    if not vacancy_condition.startswith('vac'):
        raise ValueError("vacancy_condition must be 'pris' or 'vac<index>' (e.g. 'vac0')")

    vacancy_number_str = vacancy_condition[3:]
    if not vacancy_number_str.isdigit():
        raise ValueError("vacancy_condition must be 'pris' or 'vac<index>' (e.g. 'vac0')")

    return vacancy_condition, int(vacancy_number_str)


def make_monolayer_vacancy(*,
                           size: str,
                           spec: str,
                           shift: int = 0,
                           vacancy_condition: str = 'pris') -> str:
    """Build a replicated monolayer POSCAR string, optionally with a vacancy.

    Args:
        size: Supercell size in '<dupx>x<dupy>' format (e.g., '4x4').
        spec: Unit-cell spec name that maps to '<UNITS_DIR>/<spec>.poscar'.
        shift: In-plane lattice shift index applied as shift/6 of a and b vectors.
        vacancy_condition: Either 'pris' for pristine or 'vac<index>' for a vacancy
            type index (e.g., 'vac0').

    Returns:
        POSCAR-formatted string with a descriptive header.

    Raises:
        ValueError: If any input is malformed.
    """
    dupx, dupy = _parse_supercell_size(size)
    vacancy_condition, vacancy_number = _parse_vacancy_condition(vacancy_condition)

    if not isinstance(shift, int):
        raise ValueError('shift must be an integer')

    header = f'{spec} monolayer, {size}, shift = {shift},  {vacancy_condition}'
    print('AM Making monolayer: ', header)
    
    unit = am.load('poscar', f'{UNITS_DIR}/{spec}.poscar')
    # apply shift
    unit.atoms.pos += (shift/6 * unit.box.avect) + (shift/6 * unit.box.bvect)
    unit.wrap()
    # replicate
    supercell = unit.supersize(dupx,dupy,1)
    if vacancy_number is not None:
        
        
        # remove vacancy from middle of supercell
        middle_ind = (dupx)//2
        target_pos_list = [pos + unit.box.avect*middle_ind + unit.box.bvect*middle_ind for pos in unit.atoms.pos]
        target_inds = []
        pos = supercell.atoms.pos
        for target_pos in target_pos_list:
            dist = np.linalg.norm(pos - target_pos, axis=1)
            target_ind = dist.argmin()
            target_inds.append(target_ind)
            # supercell.atoms.atype[target_ind] = 3
        
        possible_inds = get_possible_vacancies(spec)[::-1]
        try:
            vacancy_type_ind = possible_inds[vacancy_number]
        except IndexError as exc:
            raise ValueError(
                f'vacancy index {vacancy_number} is out of range for {spec}. '
                f'Possible indices are 0..{len(possible_inds) - 1}'
            ) from exc
        
        vacancy_system = am.defect.vacancy(supercell, target_inds[vacancy_type_ind])
        info = vacancy_system.dump('poscar')
    else:
        info = supercell.dump('poscar')
    output = f"{header}{info}"
    return output

