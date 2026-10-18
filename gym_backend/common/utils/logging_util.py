# common/utils/logging_util.py
import logging

# Logger အခြေခံ Config သတ်မှတ်ခြင်း
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gym_backend")

def get_logger_with_request_id(request):
    """ Controller ထဲတွင် Request အလိုက် Log မှတ်တမ်းထုတ်ပေးရန် function """
    # နောက်ပိုင်းတွင် Request ID ထည့်သွင်းလိုပါက ဤနေရာတွင် ထပ်မံပြင်ဆင်နိုင်ပါသည်
    return logger