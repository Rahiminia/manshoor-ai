const generateBtn = document.getElementById('submit_btn')
const verseTxtBox = document.getElementById('verse')
const sampleVerseTxt = document.getElementById('sample_verse')
const loading = document.getElementById('loading-wrapper')

const API_URL = 'http://127.0.0.1:4000/api/generate'

const generate = async (verse) => {
    if (!verse || verse.length == 0) {
        return ""
    }
    loading.style.visibility = 'visible'
    fetch(API_URL + `?verse=${verse}`)
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
