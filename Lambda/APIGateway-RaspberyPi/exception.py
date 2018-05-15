class Error(Exception):
    """
    例外クラス：基底クラス
    """

    def __init__(self, statusCode, error, description):
        self.statusCode = statusCode
        self.error = error
        self.description = description

class ParamError(Error):
    """
    例外クラス：パラメータエラー
    """

    def __init__(self, description):
        super().__init__(400, "invalid_request", description)