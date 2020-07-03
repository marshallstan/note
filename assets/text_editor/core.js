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
