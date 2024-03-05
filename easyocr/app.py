# Credits
# https://huggingface.co/spaces/tomofi/EasyOCR/blob/main/app.py

import PIL
import gradio as gr
from PIL import ImageDraw

import easyocr


def inference(img, lang):
    reader = easyocr.Reader(lang)
    bounds = reader.readtext(img)
    im = PIL.Image.open(img)

    dataframe = []
    draw = ImageDraw.Draw(im)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill="yellow", width=2)
        dataframe.append([
            "(%d,%d),(%d,%d),(%d,%d),(%d,%d)" % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]),
            bound[1],
            "%.2f%%" % (bound[2] * 100),
        ])

    im.save('outputs/result.jpg')

    return ['outputs/result.jpg', dataframe]


title = 'EasyOCR'
css = ".output_image, .input_image {height: 40rem !important; width: 100% !important;}"
choices = [
    "abq",
    "ady",
    "af",
    "ang",
    "ar",
    "as",
    "ava",
    "az",
    "be",
    "bg",
    "bh",
    "bho",
    "bn",
    "bs",
    "ch_sim",
    "ch_tra",
    "che",
    "cs",
    "cy",
    "da",
    "dar",
    "de",
    "en",
    "es",
    "et",
    "fa",
    "fr",
    "ga",
    "gom",
    "hi",
    "hr",
    "hu",
    "id",
    "inh",
    "is",
    "it",
    "ja",
    "kbd",
    "kn",
    "ko",
    "ku",
    "la",
    "lbe",
    "lez",
    "lt",
    "lv",
    "mah",
    "mai",
    "mi",
    "mn",
    "mr",
    "ms",
    "mt",
    "ne",
    "new",
    "nl",
    "no",
    "oc",
    "pi",
    "pl",
    "pt",
    "ro",
    "ru",
    "rs_cyrillic",
    "rs_latin",
    "sck",
    "sk",
    "sl",
    "sq",
    "sv",
    "sw",
    "ta",
    "tab",
    "te",
    "th",
    "tjk",
    "tl",
    "tr",
    "ug",
    "uk",
    "ur",
    "uz",
    "vi"
]

gr.Interface(
    inference,
    [
        gr.Image(type='filepath', label='Input'),
        gr.CheckboxGroup(choices, type="value", value=['en'], label='language'),
    ],
    [
        gr.Image(type='filepath', label='Output'),
        gr.Dataframe(headers=['coordinate', 'text', 'confidence']),
    ],
    title=title,
    css=css,
).queue(max_size=20).launch(debug=True)
