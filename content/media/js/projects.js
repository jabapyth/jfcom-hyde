
(function(){

  var each = function (selector, fn) {
    return Array.prototype.forEach.call(document.querySelectorAll(selector), fn);
  };

  var hiding = false;

  var LangLimiter = function (lang) {
    if (hiding) return;
    var node = document.createElement('div');
    document.querySelector('#header .bottom-bar').appendChild(node);
    node.innerHTML = lang;
    var that = this;
    var hideElements = function () {
      hiding = true;
      each('#main-content .project', function (node) {
        if (!node.classList.contains('lang-' + lang)) {
          node.classList.add('hidden');
        }
      });
    };
    var showElements = function () {
      hiding = false;
      each('#main-content .project.hidden', function (node) {
        node.classList.remove('hidden');
      });
    };
    node.addEventListener('click', function(){
      node.parentNode.removeChild(node);
      showElements();
    });
    hideElements();
  };

  var limit = function (e) {
    e.preventDefault();
    e.stopPropagation();

    var lang = this.innerHTML.toLowerCase();
    LangLimiter(lang);

    return false;
  };
  var langs = document.querySelectorAll('#main-content .project .lang');
  langs = Array.prototype.slice.call(langs);
  langs.forEach(function(lang) {
    lang.addEventListener('click', limit);
  });

})();
