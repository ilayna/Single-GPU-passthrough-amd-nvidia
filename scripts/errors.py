# AUTHOR: Ilay Nahman
# GITHUB: wabulu
# EMAIL : wabulubusiness@gmail.com
import colors
import utils


class Error:
    """
    Here goes all error handling and whatever
    Documentations of error codes is below
    """

    """ 
    ERROR CODES:
    101- Means couldn't open grub file (File Doesn't Exist)
    102- Distro isn't found in utils.GRUB_UPDATE_CMND so it can't execute the update grub command
    """

    @classmethod
    def report_error_msg(cls, ex, err_code=100):
        """
        Error handling is done here, the outcome depends on ex.__class__ and err_code
        :param ex: The exception
        :param err_code: The error code, if the error is expected (taken into account) this should be some other value then 100
        :rtype: None
        """
        # Error 101 is below, every error is going to have a value starting from 100, so it is easily documented later
        if ex.__class__ is FileNotFoundError:
            print(f"Error {err_code}! couldn't find {ex.filename} !")
        elif ex.__class__ is KeyError:
            print(f"Error 102! Key {ex.args} not in dictionary !")
        print(f'{colors.OKRED} Please report this as a ISSUE at {utils.REPO_LINK} !')
        colors.reset()
        input('Press enter to continue after reporting this issue !')
