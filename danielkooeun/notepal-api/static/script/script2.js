const children = $('#bottom-section').children();
let child_arr = [];

for (let i = 0; i < children.length; ++i) {
  child_arr.push(children[i].id);
}

$('#search-courses').on('input', (event) => {
  children.hide();
  let query = $(event.target).val().replace(/\s+/g, '-').toLowerCase();
  let filtered = child_arr.filter(child => child.indexOf(query) !== -1);
  filtered.forEach((child) => $(`#${child}`).show());
})