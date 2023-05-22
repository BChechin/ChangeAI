# neuro_backend

## Environments setups

### [Installed] sd_m1

Guide [for m1 processors](https://huggingface.co/docs/diffusers/optimization/mps)

1) install [custom pytorch](https://pytorch.org/get-started/locally/)  
   `conda install pytorch torchvision -c pytorch`
2) install sd:   
   `conda install -c conda-forge diffusers`
3) install python telegram bot  
   ~~`conda install -c conda-forge python-telegram-bot`~~  
   `pip install python-telegram-bot`

4) And just in case  
   ~~`conda install -c conda-forge transformers scipy ftfy accelerate`~~
   `pip install  transformers scipy ftfy accelerate`

### [Installed] sd (StableDiffusion)

pip install stable_diffusion

### sd_gpu (StableDiffusion)

No idea for now. GPT told me to install stable_diffuesion_gpu
, but I don't know how to do it.
There's no such package on pip.

### hf (HuggingFace)

pip install diffusers==0.11.1
pip install transformers scipy ftfy accelerate

### hf_inp (InPunk)

### sd_2_hf (InPunk)

### hf_

### custom_1

As
per [this colab notebook](https://colab.research.google.com/drive/19r-7IaJEZHKtbW82XJwKlOu64-KRMBp5?usp=sharing#scrollTo=ZjxbGFk9moYT)    
(Allows to run backend on Colab gpu)   
pip install diffusers==0.10.2 transformers scipy ftfy accelerate # To run Stable Diffusion   
pip install pyngrok==4.1.1 # To register our ngrok token  
pip install flask_ngrok # So we can make flask app port thru ngrok

## Making it work

### Locally - on Mac M1

This is simple:

1) create a simple telegram bot
2) set up the env
3)

### In Colab

### In Google Cloud

I originally thought that I will test it locally and then deploy it to Google Cloud.   
But now it seems that I can't test locally because M1 is a special case   
So I have to set up end test environment in Colab and then deploy it to Google Cloud.   
Maybe I should follow the "use colab gpu free" guide.
Alternatively, I can run it on the Google Cloud right away

#### test