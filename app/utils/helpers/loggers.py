from flask import current_app

def console_log(label: str ='Label', data: any =None, app=current_app) -> None:
    """
    Print a formatted message to the console for visual clarity.

    Args:
        label (str, optional): A label for the message, centered and surrounded by dashes. Defaults to 'Label'.
        data: The data to be printed. Can be of any type. Defaults to None.
    """
    
    logger = app.logger
    logger.info(f'\n\n{label:-^50}\n {data} \n{"//":-^50}\n\n')


def log_exception(label: str ='EXCEPTION', data='Nothing', app=current_app) -> None:
    """
    Log an exception with details to a logging handler for debugging.

    Args:
        label (str, optional): A label for the exception, centered and surrounded by dashes. Defaults to 'EXCEPTION'.
        data: Additional data to be logged along with the exception. Defaults to 'Nothing'.
    """

    logger = app.logger
    logger.exception(f'\n\n{label:-^50}\n {str(data)} \n {"//":-^50}\n\n')  # Log the error details for debugging