const generateBtn = document.getElementById('submit_btn')
const verseTxtBox = document.getElementById('verse')
const sampleVerseTxt = document.getElementById('sample_verse')
const loading = document.getElementById('loading-wrapper')
const paramKTxt = document.getElementById('k-param')
const seqLenTxt = document.getElementById('seq-len-txt')
const methodTxt = document.getElementById('method-select')

const METHODS = {
    GREEDY: 0,
    RANDOM: 1,
    TOP_K: 2,
}

const API_URL = 'http://127.0.0.1:4000/api/generate'

let selectedMethod = METHODS.GREEDY
paramKTxt.disabled = true;

const generate = async (verse) => {
    if (!verse || verse.length == 0) {
        return ""
    }
    loading.style.visibility = 'visible'
    const q = `?verse=${verse}&method=${methodTxt.selectedIndex}&len=${seqLenTxt.value}&k=${paramKTxt.value}`
    fetch(API_URL + q)
    .then(res => res.json())
    .then(res => {
        verseTxtBox.value = res.verse
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
