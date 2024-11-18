
from transformers import pipeline, AutoTokenizer, TFAutoModelForCausalLM
from diffusers import StableDiffusionPipeline
from googletrans import Translator

# Configuración del modelo GPT-2
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = TFAutoModelForCausalLM.from_pretrained("gpt2")
poetry_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Configuración del modelo Stable Diffusion
image_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
image_pipe.to("cpu")




def translate_to_spanish(text):
    """
    Traduce un texto en inglés al español usando googletrans.
    
    Args:
        text (str): Texto en inglés.

    Returns:
        str: Texto traducido al español.
    """
    translator = Translator()
    try:
        translated = translator.translate(text, src='en', dest='es')
        return translated.text
    except Exception as e:
        return f"Error al traducir: {e}"



def generate_poem_huggingface(theme):
    prompt = (
        f"Write a beautiful and emotional poem about '{theme}'. "
        f"The poem should be creative, deep, and full of metaphors. Here is the poem:\n\n"
    )
    try:
        result = poetry_generator(
            prompt,
            max_length=150,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=50256
        )
        english_poem = result[0]["generated_text"]
        # Traducir al español
        translated_poem = translate_to_spanish(english_poem)
        return translated_poem
    except Exception as e:
        return f"Error al generar la poesía: {e}"

def generate_image_stable_diffusion(prompt, filename="generated_image.jpg"):
    """
    Genera una imagen basada en un prompt utilizando Stable Diffusion.
    
    Args:
        prompt (str): Descripción para generar la imagen.
        filename (str): Nombre del archivo para guardar la imagen.

    Returns:
        None
    """
    try:
        image = image_pipe(prompt).images[0]
        image.save(filename)
        print(f"Imagen generada y guardada como {filename}")
    except Exception as e:
        print(f"Error al generar la imagen: {e}")

def menu():
    """
    Menú principal para que el usuario seleccione una funcionalidad.
    """
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Generar poesía (Hugging Face)")
        print("2. Generar imagen (Stable Diffusion)")
        print("3. Salir")
        choice = input("Elige una opción (1-3): ").strip()

        if choice == "1":
            theme = input("\n¿Sobre qué tema quieres que escriba una poesía? ")
            poem = generate_poem_huggingface(theme)
            print("\nPoesía Generada:\n")
            print(poem)

        elif choice == "2":
            prompt = input("\nDescribe la imagen que quieres generar: ")
            filename = input("Nombre del archivo para guardar la imagen (ejemplo: imagen.jpg): ").strip()
            if not filename:
                filename = "generated_image.jpg"
            generate_image_stable_diffusion(prompt, filename)

        elif choice == "3":
            print("\nGracias por usar el programa. ¡Hasta luego!")
            break

        else:
            print("\nOpción no válida. Por favor, elige una opción entre 1 y 3.")

if __name__ == "__main__":
    print("¡Bienvenido al proyecto de IA Generativa!")
    print("Usa este programa para generar poesía e imágenes.")
    menu()

