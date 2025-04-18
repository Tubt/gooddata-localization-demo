from os import getenv
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from gooddata_sdk import GoodDataSdk

load_dotenv()

host = getenv("GOODDATA_HOST")
token = getenv("GOODDATA_TOKEN")

def create_translation_function(target_language):
    def my_translation_function(
        to_translate: str, already_translated=True, old_translation=""
    ):
        if not to_translate:
            return ""
            
        try:
            result = GoogleTranslator(source='auto', target=target_language).translate(to_translate)
            print(f"Original text : {to_translate}")
            print(f"Translated text: {result}")
            
            # Truncate if longer than 255 characters
            if len(result) > 255:
                print(f"Warning: Translation exceeds 255 characters, truncating...")
                result = result[:255]
                print(f"Truncated text: {result}")
            
            return result
        except Exception as e:
            print(f"Translation failed: {e}")
            return old_translation

    return my_translation_function

def translate_workspace(workspace_id: str, target_language: str):
    trans_func = create_translation_function(target_language[:-3])
    sdk = GoodDataSdk.create(host, token)
    sdk.catalog_workspace.add_metadata_locale(
        workspace_id=workspace_id,
        target_language=target_language,
        translator_func=trans_func,
        set_locale=True,
    )


if __name__ == "__main__":
    translate_workspace(workspace_id="be92f91a48ea40a2b92ea9a025033092", target_language="ja-JP")
