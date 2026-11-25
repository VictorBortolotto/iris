var totalPages = 0
var actualPage = 0
var pages = []

const prediction = async () => {
  sepal_length = document.getElementById("sepal-length-input").value
  sepal_width = document.getElementById("sepal-width-input").value
  petal_length = document.getElementById("petal-length-input").value
  petal_width = document.getElementById("petal-width-input").value

  const request = {
    sepal_length: sepal_length,
    sepal_width: sepal_width,
    petal_length: petal_length,
    petal_width: petal_width,
  }

  response = await (await predict(request)).json()

  document.getElementById("specie").value = response.species
  document.getElementById("setosa-probalitie").value = response.probabilities["Iris Setosa"]
  document.getElementById("versicolor-probalitie").value = response.probabilities["Iris Versicolor"]
  document.getElementById("virginica-probalitie").value = response.probabilities["Iris Virginica"]

  getStatsIris()
}

const getStatsIris = async () => {
  const response = await (await get_stats()).json()

  document.getElementById("total-stat").innerText = response.data.total_classifications
  document.getElementById("setosa-total").innerText = response.data.setosa_count ? response.data.setosa_count : 0
  document.getElementById("setosa-perc").innerText = response.data.setosa_percentage ? response.data.setosa_percentage + '%' : 0 + '%'
  document.getElementById("versicolor-total").innerText = response.data.versicolor_count ? response.data.versicolor_count : 0
  document.getElementById("versicolor-perc").innerText = response.data.versicolor_percentage ? response.data.versicolor_percentage + '%' : 0 + '%'
  document.getElementById("virginica-total").innerText = response.data.virginica_count ? response.data.virginica_count : 0
  document.getElementById("virginica-perc").innerText = response.data.virginica_percentage ? response.data.virginica_percentage + '%' : 0 + '%'
}

const getAllPredctions = async () => {
  const response = await (await get_all_predctions()).json()

  if (response.data === undefined) {
    showSnackbar(response.message, 'alert')
    showNotFoundImageOrHistoryList([])
  } else {
    fillPage(response.data, 0)
    actualPage = 0
    showNotFoundImageOrHistoryList(response.data)
    updatePageCaption(actualPage)
    showSnackbar(response.message, 'success')
  }
}

const onClickHistory = () => {
  predictionArea = document.getElementById("prediction")
  historyArea = document.getElementById("history")
  historySearchArea = document.getElementById("history-search-area")
  historyPageControl = document.getElementById("history-page-control")

  predictionArea.style.display = 'none'
  historyArea.style.display = 'flex'
  historySearchArea.style.display = 'flex'
  historyPageControl.style.display = 'flex'

  getAllPredctions()
}

const onClickSearch = () => {
  predictionArea = document.getElementById("prediction")
  historyArea = document.getElementById("history")
  historySearchArea = document.getElementById("history-search-area")
  historyPageControl = document.getElementById("history-page-control")

  predictionArea.style.display = 'flex'
  document.getElementById("history-list").innerHTML = ''
  historyArea.style.display = 'none'
  historySearchArea.style.display = 'none'
  historyPageControl.style.display = 'none'
}

const onClickSearchButton = async() => {
  searchInput = document.getElementById("search-input").value

  let html = ''
  
  if (searchInput.trim() !== "" && !isNaN(searchInput)) {
    const response = await (await get_predction_by_id(searchInput)).json()
    pages = []

    if (response.data === undefined) {
      showSnackbar(response.message, 'alert')
      return
    }
    html = card(response.data)
    
    cleanHistoryList()
    document.getElementById("history-list").innerHTML = ''
    document.getElementById("history-list").innerHTML += html
    showSnackbar(response.message, 'success')
  } else {
    const response = await (await get_all_predctions(searchInput)).json()

    if (response.data === undefined) {
      showSnackbar(response.message, 'alert')
      return
    }

    cleanHistoryList()
    showSnackbar(response.message, 'success')
    fillPage(response.data, 0)
  }

  actualPage = 0
  updatePageCaption(actualPage)
}

const fillPage = (predictions, position) => {
  let board = document.getElementById('history-list')
  let pageSize = predictions[position].length
  let html = ''
  pages = predictions
  for (i = 0; i < pageSize; i++) {
    predictionItem = predictions[position][i]
    html += card(predictionItem)
  }

  board.innerHTML += html
  updatePageCaption(position)
}

const onClickPrevious = () => {
  actualPage -= 1
  
  if (actualPage < 0) {
    actualPage = 0
  }

  cleanHistoryList()
  fillPage(pages, actualPage)
  updatePageCaption(actualPage)
}

const onClickNext = () => {
  actualPage += 1

  if (actualPage == pages.length) {
    actualPage = 0
  }
  
  cleanHistoryList()
  fillPage(pages, actualPage)
  updatePageCaption(actualPage)
}

const cleanHistoryList = () => {
  let historyList = document.getElementById('history-list')
  historyList.innerHTML = ""
}

const updatePageCaption = (actualPage) => {
  let pagesCaption = document.getElementById('pages-caption')
  let pageNumber = actualPage
  let totalPages = 0

  if (actualPage < 1) {
    pageNumber = 1
  } else {
    pageNumber += 1
  }

  if (pages.length === 0){
    totalPages = 1 
  } else {
    totalPages = pages.length
  }

  pagesCaption.innerText = pageNumber + ' / ' + totalPages
}

const showNotFoundImageOrHistoryList = (pages) => {
  let historyList = document.getElementById('history-list')
  let notFound = document.getElementById('not-found')

  if (pages.length === 0) {
    notFound.style.display = 'flex'
    historyList.style.display = 'none'
  } else {
    notFound.style.display = 'none'
    historyList.style.display = 'grid'
  }
}