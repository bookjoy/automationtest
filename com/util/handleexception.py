
class HandleException(BaseException):
        def __init__(self):
                pass
                
	def NOT_FOUND_ERR(self, msg):
                print 'Error Ocurred:', msg

        def NOT_FOUND_EXCEPTION(self, exception):
                print 'Error Ocurred:', exception


