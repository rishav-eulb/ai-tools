import os
class MMSBatchModel():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MMSBatchModel, cls).__new__(cls)
            cls.load_model(cls)
        return cls.instance

    def load_model(self):
        """ Loads the model. This method is called only once when the model is first loaded."""
        # Step 1: Clone fairseq-py and install the latest version
        !mkdir "temp_dir"
        !git clone https: // github.com/pytorch/fairseq

        # Change current working directory
        !pwd
        %cd "/content/fairseq"
        !pip install - -editable ./
        !pip install tensorboardX

        # Step 2: Download MMS model
        # Uncomment to download your preferred model. In this example, we use MMS-FL102 for demo purposes.
        # For better model quality and language coverage, user can use MMS-1B-ALL model instead.
        # (Please note that MMS-1B-ALL requires more RAM, so please use Colab-Pro instead of Colab-Free).

        # MMS-1B:FL102 model - 102 Languages - FLEURS Dataset
        !wget - P ./models_new 'https://dl.fbaipublicfiles.com/mms/asr/mms1b_fl102.pt'

        # # MMS-1B:L1107 - 1107 Languages - MMS-lab Dataset
        # !wget -P ./models_new 'https://dl.fbaipublicfiles.com/mms/asr/mms1b_l1107.pt'

        # # MMS-1B-all - 1162 Languages - MMS-lab + FLEURS + CV + VP + MLS
        # !wget -P ./models_new 'https://dl.fbaipublicfiles.com/mms/asr/mms1b_all.pt'

    def inference(self, request):
        """ Performs inference on the given request. This method is called for every request."""
        audio_path = request.audio_path
        lang = request.lang

        # Step 3: Run Inference and transcribe your audio(s)
        os.environ["TMPDIR"] = '/content/temp_dir'
        os.environ["PYTHONPATH"] = "."
        os.environ["PREFIX"] = "INFER"
        os.environ["HYDRA_FULL_ERROR"] = "1"
        os.environ["USER"] = "micro"

        # Run the MMS inference command
        cmd = f"python examples/mms/asr/infer/mms_infer.py --model \"/content/fairseq/models_new/mms1b_fl102.pt\" --lang \"{lang}\" --audio \"{audio_path}\""
        output = os.popen(cmd).read()
        # Implement the parsing logic based on the output format
       

        return output

      
