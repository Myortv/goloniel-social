from typing import Tuple, Optional, List, Any


def create_optional_filters(
    index: Optional[int] = 1,
    **kwargs,
) -> Tuple[List[str], List[Any], int]:
    filters = list()
    args = list()
    for key, value in kwargs.items():
        if not value:
            continue
        filters.append(f'{key} = ${index}')
        args.append(value)
        index += 1
    if not filters:
        return ([], [], index)
    return (filters, args, index)
