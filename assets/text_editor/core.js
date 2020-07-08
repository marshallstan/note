var FontStyle = Quill.import('attributors/style/font');
FontStyle.whitelist = null;
Quill.register(FontStyle, true);

var SizeStyle = Quill.import('attributors/style/size');
SizeStyle.whitelist = null;
Quill.register(SizeStyle, true);

var quill = new Quill('#editor', {
  modules: {
    syntax: true,
    toolbar: false,
  },
  theme: 'snow'
});

quill.on('selection-change', function(){
  pyOnFormatChanged(quill.getFormat());
});

let editor = quill.container.firstChild;
quill.loadContent = function(value) {
  quill.setContents([]);
  editor.innerHTML = value;
};

quill.on('text-change', function(_,__,source){
  if(source === 'api') {
    return;
  }
  pyOnContentChanged(editor.innerHTML);
});

let searcher = new Searcher(quill);
quill.findAll = function(keyword) {
  searcher.findAll(keyword);
};
