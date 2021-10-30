const btnDelete = document.querySelectorAll('.btn-delete')

if (btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('¿ Esta seguro que desea eliminar este registro ?')) {
        e.preventDefault();
      }
    });
  });

}