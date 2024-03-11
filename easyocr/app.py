# Credits
# https://huggingface.co/spaces/tomofi/EasyOCR/blob/main/app.py

# Allowed environment variables
# EASYOCR_TITLE: title of the app
# EASYOCR_ALLOWED_LANGS: comma separated list of languages to be allowed
# EASYOCR_DEFAULT_LANGS: comma separated list of languages to be selected by default
# EASYOCR_NO_DEBUG: set to "true" to disable debug mode
# EASYOCR_OUTPUT_FOLDER: set to the folder where the output images will be saved
# EASYOCR_THRESHOLD: set to the threshold for the confidence level

import os
import time
from typing import List

import easyocr
import gradio as gr
from PIL import ImageDraw, Image

# Output folder
output_folder = os.getenv("EASYOCR_OUTPUT_FOLDER")
if not output_folder:
    output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Debug mode
no_debug = os.getenv("EASYOCR_NO_DEBUG") != "true"

# Title
title = os.getenv("EASYOCR_TITLE")
if not title:
    title = "EasyOCR"

threshold = os.getenv("EASYOCR_THRESHOLD")
if threshold:
    threshold = float(threshold)  # make a panic if it's not a number

# region Supported languages

# https://www.jaided.ai/easyocr/
# Array.from(document.querySelectorAll('table tr'))
#   .slice(1)
#   .map(tr => `    (${Array.from(tr.querySelectorAll('td')).map(td => `"${td.innerText}"`).join(",")}),\n`)
#   .join('')
supported_lang_set = (
    # ("Language","Code Name"),
    ("Abaza", "abq"),
    ("Adyghe", "ady"),
    ("Afrikaans", "af"),
    ("Angika", "ang"),
    ("Arabic", "ar"),
    ("Assamese", "as"),
    ("Avar", "ava"),
    ("Azerbaijani", "az"),
    ("Belarusian", "be"),
    ("Bulgarian", "bg"),
    ("Bihari", "bh"),
    ("Bhojpuri", "bho"),
    ("Bengali", "bn"),
    ("Bosnian", "bs"),
    ("简体中文", "ch_sim"),
    ("繁體中文", "ch_tra"),
    ("Chechen", "che"),
    ("Czech", "cs"),
    ("Welsh", "cy"),
    ("Danish", "da"),
    ("Dargwa", "dar"),
    ("German", "de"),
    ("English", "en"),
    ("Spanish", "es"),
    ("Estonian", "et"),
    ("Persian (Farsi)", "fa"),
    ("French", "fr"),
    ("Irish", "ga"),
    ("Goan Konkani", "gom"),
    ("Hindi", "hi"),
    ("Croatian", "hr"),
    ("Hungarian", "hu"),
    ("Indonesian", "id"),
    ("Ingush", "inh"),
    ("Icelandic", "is"),
    ("Italian", "it"),
    ("Japanese", "ja"),
    ("Kabardian", "kbd"),
    ("Kannada", "kn"),
    ("Korean", "ko"),
    ("Kurdish", "ku"),
    ("Latin", "la"),
    ("Lak", "lbe"),
    ("Lezghian", "lez"),
    ("Lithuanian", "lt"),
    ("Latvian", "lv"),
    ("Magahi", "mah"),
    ("Maithili", "mai"),
    ("Maori", "mi"),
    ("Mongolian", "mn"),
    ("Marathi", "mr"),
    ("Malay", "ms"),
    ("Maltese", "mt"),
    ("Nepali", "ne"),
    ("Newari", "new"),
    ("Dutch", "nl"),
    ("Norwegian", "no"),
    ("Occitan", "oc"),
    ("Pali", "pi"),
    ("Polish", "pl"),
    ("Portuguese", "pt"),
    ("Romanian", "ro"),
    ("Russian", "ru"),
    ("Serbian (cyrillic)", "rs_cyrillic"),
    ("Serbian (latin)", "rs_latin"),
    ("Nagpuri", "sck"),
    ("Slovak", "sk"),
    ("Slovenian", "sl"),
    ("Albanian", "sq"),
    ("Swedish", "sv"),
    ("Swahili", "sw"),
    ("Tamil", "ta"),
    ("Tabassaran", "tab"),
    ("Telugu", "te"),
    ("Thai", "th"),
    ("Tajik", "tjk"),
    ("Tagalog", "tl"),
    ("Turkish", "tr"),
    ("Uyghur", "ug"),
    ("Ukranian", "uk"),
    ("Urdu", "ur"),
    ("Uzbek", "uz"),
    ("Vietnamese", "vi")
)
supported_lang_map = {}
for i in supported_lang_set:
    supported_lang_map[i[1]] = i


def format_langs_from_env(from_env_name: str, default):
    lang_set = []
    langs_from_envar = os.getenv(from_env_name)
    if langs_from_envar:
        langs = langs_from_envar.split(",")
        for lang in langs:
            lang = lang.strip()
            if lang and supported_lang_map[lang]:
                lang_set.append(supported_lang_map[lang])
    if len(lang_set) == 0:
        return default
    return lang_set


allowed_lang_set = format_langs_from_env("EASYOCR_ALLOWED_LANGS", supported_lang_set)
default_lang_set = format_langs_from_env("EASYOCR_DEFAULT_LANGS", [])

default_langs = []
for i in default_lang_set:
    default_langs.append(i[1])


# endregion

cached_reader = {}
if len(default_langs) > 0:
    print('Initializing default reader...')
    cached_reader[','.join(default_langs)] = easyocr.Reader(default_langs)


def inference(img: str, languages: List[str]):
    if not img:
        return []

    reader_key = ','.join(languages)
    if reader_key not in cached_reader:
        start = time.time()
        cached_reader[reader_key] = easyocr.Reader(languages)
        print('Reader Initialization takes', time.time() - start, 's')
    reader = cached_reader[reader_key]

    start = time.time()
    bounds = reader.readtext(img)
    print('Prediction takes', time.time() - start, 's')

    start = time.time()
    im = Image.open(img)

    dataframe = []
    draw = ImageDraw.Draw(im)
    for bound in bounds:
        if bound[2] < threshold:
            continue
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill="yellow", width=2)
        dataframe.append([
            "(%d,%d),(%d,%d),(%d,%d),(%d,%d)" % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]),
            bound[1],
            "%.2f%%" % (bound[2] * 100),
        ])

    image_filepath = os.path.join(output_folder, "result.jpg")  # dynamically change the file name?
    im.save(image_filepath)

    print('Postprocess takes', time.time() - start, 's')

    return [image_filepath, dataframe]


# language=css
css = """
.output_image, .input_image {
    height: 40rem !important; 
    width: 100% !important;
}

@keyframes BoxerFadeOut {
    to {
        opacity: 0;
    }
}

#OutputImage {
    .image-container {
        position: relative;
        .boxer {
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 0;
            border: 2px solid yellow;
            background-color: aqua;
            opacity: 1;
            z-index: 1001;
            &.dim {
                animation-name: BoxerFadeOut;
                animation-duration: 0.5s;
                animation-fill-mode: forwards;
                animation-timing-function: ease-in-out;
                animation-iteration-count: 1;
            }
        }
    }
}
#OutputDataframe {
    tr {
        td:nth-child(1), td:nth-child(1) {
            display: none;
        }
    }
}
"""

# language=javascript
javascript = """
() => {
    window.addEventListener('keypress', e => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
            e.preventDefault();
            document.getElementById('SubmitButton')?.click();
        }
    });

    // ---

    /**
     * @typedef X
     * @type number
     */
    /**
     * @typedef Y
     * @type number
     */
     
     let highlightTimer = -1;
     
    /**
     * @param {[X, Y]} p0
     * @param {[X, Y]} p1
     * @param {[X, Y]} p2
     * @param {[X, Y]} p3
     * @example (254,58),(280,58),(280,86),(254,86)
     */
    function highlight(p0, p1, p2, p3) {
        clearTimeout(highlightTimer);
        /** @type HTMLImageElement */
        const ele = document.querySelector('#OutputImage img');
        if (!ele) {
            alert('Can NOT find the image container');
            return;
        }
        const { naturalWidth, naturalHeight } = ele;
        
        /** @type HTMLDivElement */
        let boxer = ele.parentElement.querySelector('.boxer');
        if (!boxer) {
            boxer = document.createElement('div');
            boxer.classList.add('boxer');
            ele.parentElement.append(boxer);
        }
        boxer.style.left = `${p0[0] / naturalWidth * 100}%`;
        boxer.style.top = `${p0[1] / naturalHeight * 100}%`;
        boxer.style.width = `${Math.abs(p2[0] - p0[0]) / naturalWidth * 100}%`;
        boxer.style.height = `${Math.abs(p2[1] - p0[1]) / naturalHeight * 100}%`;
        boxer.classList.remove('dim');
        highlightTimer = setTimeout(() => {
            boxer.classList.add('dim');
        });
    }
    
    function findTR(ele) {
        if (!ele || ele.tagName === 'TABLE' || ele.tagName === 'BODY') {
            return undefined;
        }
        if (ele.tagName === 'TR') {
            return ele;
        }
        return findTR(ele.parentElement);
    }
    
    const dataframes = document.querySelector('#OutputDataframe');
    if (!dataframes) {
        alert('Can NOT find the dataframes');
        return;
    }
    dataframes.addEventListener('click', e => {
        console.log('onclick:', e.target);
        const tr = findTR(e.target);
        if (!tr) {
            return;
        }
        const coordinate = Array.from(tr.querySelectorAll('td'))[0]?.innerText?.trim();
        if (!coordinate || !/^(\(\d+,\d+\),){3}\(\d+,\d+\)$/.test(coordinate)) {
            return;
        }
        const [p0, p1, p2, p3] = /** @type {[X, Y][]} */ 
            coordinate.split('),(').map(p => p.replace(/[()]/g, '').split(',').map(Number));
        if (!p0 || !p1 || !p2 || !p3) {
            return;
        }
        highlight(p0, p1, p2, p3);
    });
}
"""

gr.Interface(
    inference,
    [
        gr.Image(type="filepath", label="Input"),
        gr.CheckboxGroup(allowed_lang_set, type="value", value=default_langs, label="language"),
    ],
    [
        gr.Image(type="filepath", label="Output", elem_id="OutputImage"),
        gr.Dataframe(headers=["coordinate", "text", "confidence"], elem_id="OutputDataframe"),
    ],
    title=title,
    css=css,
    js=javascript,
    allow_flagging="never",
    submit_btn=gr.Button("Submit", variant="primary", elem_id="SubmitButton"),
).queue(max_size=20).launch(debug=no_debug)
