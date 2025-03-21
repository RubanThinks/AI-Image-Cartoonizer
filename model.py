from diffusers import StableDiffusionInstructPix2PixPipeline
model_id = "instruction-tuning-sd/cartoonizer"
pipeline = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id)
pipeline.save_pretrained("./local-cartoonizer")
