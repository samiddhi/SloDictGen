from typing import Callable, Any, Iterable, List
from tqdm import tqdm
from icecream import ic
from utils.json_utils import extend_json_array

def batch_and_process(
        data: Any,
        process_func: Callable[[Any], Any],
        length_func: Callable[[Any], int],
        max_length: int,
        batch_func: Callable[[Iterable[Any]], None],
        log_path: str = None,
        _track: bool = False,
        _batch_limit: int = float('inf')
) -> None:
    """
    Batch data by specified size into list, process data before batching, pass batch to specified ``batch_func`` arg

    :param data: The input data to be processed.
    :param process_func: The function to process each element of the data.
    :param length_func: The function to get the length of each processed element.
    :param max_length: The maximum length of each batch.
    :param batch_func: The function to pass each batch into.
    :param _track: ``True`` prints total batch and length counts
    :param _batch_limit: ``int`` limits total batch count for testing purposes
    :return: None
    """
    current_batch = []
    current_batch_data = []
    current_length = 0
    batch_count = 0
    length_count = 0

    for item in tqdm(data):
        processed_item = item if process_func is None else process_func(item)
        item_length = length_func(processed_item)

        if current_length + item_length <= max_length:
            current_batch.append(processed_item)
            current_length += item_length
            current_batch_data.append(item)
        else:
            batch_func(current_batch)
            if log_path:
                extend_json_array(log_path, current_batch_data)
            batch_count += 1
            length_count += current_length
            current_batch = [processed_item]
            current_length = item_length
            current_batch_data= [item]
            if _batch_limit <= batch_count:
                break

    if current_batch:
        batch_func(current_batch)
        if log_path:
            extend_json_array(log_path, current_batch_data)
        batch_count += 1
        length_count += current_length

    if _track:
        print(f'Total Batches: {batch_count}')
        print(f'Total Length: {length_count}')


if __name__ == "__main__":
    def upp(s: str):
        return s.upper()
    def werd(l: List[str]):
        print("".join(l))

    batch_and_process(
        data="woa you may get the big cow mad bro",
        process_func=upp,
        length_func=len,
        max_length=4,
        batch_func=werd
    )