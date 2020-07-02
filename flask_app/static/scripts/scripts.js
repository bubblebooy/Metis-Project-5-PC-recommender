let inpts = document.getElementById('form-watch').getElementsByTagName('input')

for (const inpt of inpts) {
  inpt.addEventListener('change', () => document.getElementById("form").submit() )
}

let selected_builds_list = document.getElementById('selected_build_list').getElementsByTagName('li')

for (const item of selected_builds_list) {
  item.addEventListener('click', () => {
    document.getElementById('remove_build').value = item.getAttribute('value')
    document.getElementById("form").submit()
  } )
}

let buildSelector = document.getElementById('build-selector')
buildSelector.addEventListener('change', () => document.getElementById("form").submit() )

let recommendations = document.getElementsByClassName("recommendation")
for (const recommendation of recommendations) {
  recommendation.addEventListener('click', () =>  {
    buildSelector.value = recommendation.getAttribute('value')
    document.getElementById("form").submit()
  } )
}
