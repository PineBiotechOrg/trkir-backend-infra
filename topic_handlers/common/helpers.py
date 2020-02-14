def on_send_success(record_metadata):
    # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
    print("sent to topic ", record_metadata.topic)


def on_send_error(exception):
    # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
    print('error: ', exception)


def convert_to_dict(columns, results):
    """
    This method converts the resultset from postgres to dictionary
    interates the data and maps the columns to the values in result set and converts to dictionary
    :param columns: List - column names return when query is executed
    :param results: List / Tuple - result set from when query is executed
    :return: list of dictionary- mapped with table column name and to its values
    """

    columns = [col.name for col in columns]
    if isinstance(results, list):
        return [dict(zip(columns, value)) for value in results]
    elif isinstance(results, tuple):
        return dict(zip(columns, results))
