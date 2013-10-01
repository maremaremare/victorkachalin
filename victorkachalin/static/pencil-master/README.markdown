# Pencil
Simple jQuery HTML5 WYSIWYG

## Author
Ilya Shalyapin, www.ishalyapin.ru, ishalyapin@gmail.com

## Status
Unstable

## Features
 - AJAX image uploading
 - Internationalization: english and russian languages are in the box.
 - Plugins

## Browser compatibility
Firefox, Opera, Chome.

## Requirements
 - jQuery (http://jquery.com/)
 - JQuery Form Plugin (http://malsup.com/jquery/form/)

## TODO
 - Fix IE7/8/9: link, image
 - AJAX upload with thumbnails

## USAGE
    <!DOCTYPE HTML>
    <html>
        <head>
            <script src="jquery.min.js"></script>
            <script src="jquery.form.js"></script>
            <script src="pencil.js"></script>
            <link rel="stylesheet" type="text/css" href="pencil.css" />
            <script>
                $(function(){
                    $('#editor').pencil({'uploaderUrl':'/my-uploader/'});
                });
            </script>
        </head>
        <body>
            <textarea id="editor">
        </body>
    </html>

### AJAX image uploader

Uploader should return JSON (content_type='application/json; charset=utf-8'):

    {'url': '/media/123.jpg'}

In case of error:

    {'error':'some error message'}

## Internationalization

Pencil accepts 'language' argument:

    <script>
        $(function(){
            $('#editor').pencil({language: 'ru'});
        });
    </script>

English and russian languages are available in the box.

If you would like to add an other language, do the following:

    Pencil.prototype.translations['my'] = {
        'toolbar.bold': 'my value',
        ...
    }

then initialize Pencil with your language:

    $('#editor').pencil({language: 'my'});

## Plugins

For example you want to add a button to the toolbar.

Create pencil.mybutton.js


    Pencil.prototype.addPlugin('mybutton', function(){
        var html = "<b>HELLO WORLD</b>";
        this.insertHtml(html);
        return false;
    });
    Pencil.prototype.translations['en']['toolbar.mybutton'] = 'My Button';
    Pencil.prototype.translations['ru']['toolbar.mybutton'] = 'Моя кнопка';
    $('#editor3').pencil({language:'ru'});


Create pencil.mybutton.css:

    .pencil_toolbar_button__mybutton {background-image: url(img/toolbar/mybutton.png;}
