// input elements
const generateBtn = document.getElementById('submit_btn')
const verseTxtBox = document.getElementById('verse')
const sampleVerseTxt = document.getElementById('sample_verse')
const paramKTxt = document.getElementById('k-param')
const seqLenTxt = document.getElementById('seq-len-txt')
const methodTxt = document.getElementById('method-select')
const modelTxt = document.getElementById('model-select')
const tempTxt = document.getElementById('temperature')

// parameter sections
const gptParamSection = document.getElementById('gpt-params')
const lstmParamSection = document.getElementById('lstm-params')

// warnings & errors
const gptWeightWarning = document.getElementById('gpt-weight-warning')
const gptWeightError = document.getElementById('gpt-weight-error')

// loading element
const loading = document.getElementById('loading-wrapper')


const MODELS = {
    GPT: 0,
    LSTM: 1,
}

const METHODS = {
    GREEDY: 0,
    RANDOM: 1,
    TOP_K: 2,
}

const API_URL = 'http://127.0.0.1:4000/api/generate'

let selectedMethod = METHODS.GREEDY

const showParams = (modelType) => {
    switch (modelType) {
        case MODELS.GPT:
            lstmParamSection.hidden = true
            gptWeightWarning.hidden = false
            gptParamSection.hidden = false
            break
        case MODELS.LSTM:
            lstmParamSection.hidden = false
            gptWeightWarning.hidden = true
            gptParamSection.hidden = true
    }
}

paramKTxt.disabled = true;
showParams(MODELS.GPT)

const generate = async (verse) => {
    if (!verse || verse.length == 0) {
        return ""
    }
    loading.style.visibility = 'visible'
    const q = `?model=${modelTxt.selectedIndex}&temperature=${tempTxt.value}&verse=${verse}&method=${methodTxt.selectedIndex}&len=${seqLenTxt.value}&k=${paramKTxt.value}`
    fetch(API_URL + q)
    .then(res => {
        return new Promise((resolve) => res.json()
        .then((jsonData) => resolve({
            status: res.status,
            ok: res.ok,
            jsonData,
            })
        ))
    })
    .then(data => {
        if (data.ok) {
            verseTxtBox.value = data.jsonData.verse;
        } else {
            if (data.jsonData?.message === "model onnx file not found") {
                gptWeightError.hidden = false;
                sampleVerseTxt.classList.add('error');
                setTimeout(() => {
                    gptWeightError.hidden = true;
                    sampleVerseTxt.classList.remove('error');
                }, 2000);
            }
        }
    })
    .catch(err => console.log(err))
    .finally(() => {
        loading.style.visibility = 'hidden'
    })
}

const clickHandler = () => {
    const sampleVerse = sampleVerseTxt.value
    generate(sampleVerse)
}

generateBtn.addEventListener('click', clickHandler)

methodTxt.addEventListener('change', (e) => {
    selectedMethod = e.target.selectedIndex
    if (selectedMethod === 2) {
        paramKTxt.disabled = false;
    }
    else {
        paramKTxt.disabled = true;
    }
})

modelTxt.addEventListener('change', e => {
    showParams(e.target.selectedIndex)
})