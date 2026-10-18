import datetime
# JWT သုံးရန် 'pip install python-jose' သို့မဟုတ် 'pip install pyjwt' သွင်းထားရန်လိုပါမည်
# လောလောဆယ် functional ဖြစ်အောင် ရိုးရိုးပဲ ရေးပေးထားပါတယ်
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Password မှန်ကန်မှု ရှိမရှိ စစ်ဆေးရန် """
    return plain_password == hashed_password

def create_access_token(data: dict) -> str:
    """ JWT Access Token ထုတ်ပေးရန် """
    # မိမိ၏ တကယ့် Token logic ကို ဒီမှာ ထည့်သွင်းနိုင်သည်
    return "generated_jwt_token_here_xyz123"