(function () {

  var set_view = function () {
    document.body.className = location.hash.slice(1) || 'blocks';
  };
  window.addEventListener('hashchange', set_view, false);
  set_view();

  var make_viewer = function (name) {
    return function () {
      document.body.className = name || 'blocks';
    };
  };
  // because hashchange takes too long...
  var views = ['full', 'blocks', 'titles'];
  var i = views.length;
  while (--i) {
    document.getElementsByClassName('blog-' + views[i])[0].addEventListener('click', make_viewer(views[i]), false);
  }

})();
