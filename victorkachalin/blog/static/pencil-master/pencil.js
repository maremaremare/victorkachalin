/*
Pencil - simple HTML5 WISIWYG.

Author: Ilya Shalyapin
Website: www.ishalyapin.ru
Email: ishalyapin@gmail.com

Requirements:
    - jQuery (http://jquery.com/)
    - JQuery Form Plugin (http://malsup.com/jquery/form/)
*/

/*jslint browser:true, nomen:true, indent: 4*/
/*global jQuery, Pencil, alert*/


function Pencil(textarea, options) {
    "use strict";

    this.default_language = 'en';
    var _this = this;
    this.$textarea = $(textarea);

    if (options === undefined) {
        this.options = {};
    } else {
        this.options = options;
    }
    this.options.uploaderUrl = this.options.uploaderUrl || '/upload/';
    this.toolbarButtons = this.options.toolbarButtons || this.toolbarButtons;
    this.language = this.options.language || this.default_language;

    this.$textarea.wrap('<div class="pencil_wrapper pencil-lang_' + this.language + '"></div>');
    this.$wrapper = this.$textarea.parent('.pencil_wrapper');
    this.$wrapper.width(this.$textarea.width());

    $(textarea).after('<div class="pencil_div" style="overflow-y: scroll;"></div>');
    this.$div = this.$textarea.siblings('.pencil_div');
    this.$div.attr('contenteditable', 'true');
    this.$div.html(this.$textarea.html());
    this.$div.width(this.$textarea.width() - (this.$div.outerWidth() - this.$div.width()));
    this.$div.height(this.$textarea.height() - (this.$div.outerHeight() - this.$div.height()));
    this.$div.blur(function () {
        if (_this.mode === 'visual') {
            _this.$textarea.val(_this.$div.html());
        }
    });

    this.$div.bind('keyup click', function (e) {
        var $node = $(_this.getSelectionStartNode());
        if ($node.is('a')) {

            _this.showModal('link-form');
            $('.pencil_modal [name=name]').val($node.text());
            $('.pencil_modal [name=url]').val($node.attr('href'));

            $('.pencil_modal_submit').click(function () {
                var name = $('.pencil_modal [name=name]').val();
                var url = $('.pencil_modal [name=url]').val();
                $node.text(name);
                $node.attr('href', url);
                _this.closeModal();
            });
        }
    });

    this.$textarea.before(this.getTemplate('toolbar'));
    this.$div.after(this.getTemplate('switch'));

    this.templates['image-form'] = this.templates['image-form'].replace('{{UPLOADER_URL}}', this.options.uploaderUrl);

    // AJAX image uploading
    $('.pencil_modal input[name=file]').live('change', function () {
        var $form = $('.pencil_modal form');

        $('input[name=url]', $form).val('');
        $('.pencil_modal_throbber', $form).remove();
        $('.pencil_modal_thumb', $form).remove();

        var throbber = '<div class="pencil_modal_throbber"></div>';
        $(throbber).insertAfter($('input[name=file]'), $form);

        $form.ajaxSubmit(function (data) {
            //Opera hack
            data = data.replace(/^<pre>/, '').replace(/<\/pre>$/, '');
            //IE hack
            data = data.replace(/^<PRE>/, '').replace(/<\/PRE>$/, '');
            try {
                data = JSON.parse(data);
            } catch (err) {
                alert('Не удалось обработать ответ от сервера.');
            }

            if (data.error) {
                alert(data.error);
                return;
            }

            var url = $('.pencil_modal [name=url]').val();
            _this.closeModal();
            _this.restoreSelection();
            _this.insertHtml('<img src="' + data.url + '" />');
        });
    });

    for (var i=0; i<this.toolbarButtons.length; ++i){
        var name = this.toolbarButtons[i];
        this.addToolbarButton(name);
        this.getButton(name).click( $.proxy(this.plugins[name], this) );
    }

    this.$div.blur(function () {
        _this.saveSelection();
    });

    $('.pencil_switch_html', this.$wrapper).click(function () {
        _this.htmlMode();
        return false;
    });
    $('.pencil_switch_visual', this.$wrapper).click(function () {
        _this.visualMode();
        return false;
    });

}
Pencil.prototype = {

    toolbarButtons: [
        'bold',
        'italic',
        'strike',
        'underline',
        'left',
        'center',
        'right',
        'ol',
        'ul',
        'h1',
        'h2',
        'h3',
        'image',
        'link',
        'video',
        'undo',
        'redo',
        'removeformat'
    ],

    plugins: {
        'bold': function () {
            document.execCommand('Bold', false, true);
            this.$div.focus();
            return false;
        },
        'italic': function () {
            document.execCommand('Italic', false, true);
            this.$div.focus();
            return false;
        },
        'strike': function () {
            document.execCommand('StrikeThrough', false, true);
            this.$div.focus();
            return false;
        },
        'underline': function () {
            document.execCommand('Underline', false, true);
            this.$div.focus();
            return false;
        },
        'left': function () {
            document.execCommand('JustifyLeft', false, true);
            this.$div.focus();
            return false;
        },
        'center': function () {
            document.execCommand('JustifyCenter', false, true);
            this.$div.focus();
            return false;
        },
        'right': function () {
            document.execCommand('JustifyRight', false, true);
            this.$div.focus();
            return false;
        },
        'ol': function () {
            document.execCommand('InsertOrderedList', false, true);
            this.$div.focus();
            return false;
        },
        'ul': function () {
            document.execCommand('InsertUnorderedList', false, true);
            this.$div.focus();
            return false;
        },
        'h1': function () {
            document.execCommand('RemoveFormat', false, true);
            document.execCommand('FormatBlock', false, '<h1>');
            this.$div.focus();
            return false;
        },
        'h2': function () {
            document.execCommand('RemoveFormat', false, true);
            document.execCommand('FormatBlock', false, '<h2>');
            this.$div.focus();
            return false;

        },
        'h3': function () {
            document.execCommand('RemoveFormat', false, true);
            document.execCommand('FormatBlock', false, '<h3>');
            this.$div.focus();
            return false;
        },
        'image': function() {
            this.showModal('image-form');
            var _this = this;
            $('.pencil_modal_submit').click(function () {
                var url = $('.pencil_modal [name=url]').val();
                _this.closeModal();

                _this.restoreSelection();
                _this.insertHtml('<img src="' + url + '" />');
            });
        },
        'link': function() {
            this.showModal('link-form');
            var text = this.getSelectedText();
            if (text) {
                $('.pencil_modal [name=name]').val(text);
            }
            var _this = this;
            $('.pencil_modal_submit').click(function () {
                var name = $('.pencil_modal [name=name]').val();
                var url = $('.pencil_modal [name=url]').val();
                _this.closeModal();

                _this.restoreSelection();
                _this.insertHtml('<a href="' + url + '">' + name + '</a>');
            });
        },
        'video': function (){
            this.showModal('video-form');
            var _this = this;
            $('.pencil_modal_submit').click(function () {
                var html = $('.pencil_modal [name=html_code]').val();
                _this.closeModal();

                _this.restoreSelection();
                _this.insertHtml(html);
            });
        },
        'undo': function () {
            document.execCommand('Undo', false, true);
            this.$div.focus();
            return false;
        },
        'redo': function () {
            document.execCommand('Redo', false, true);
            this.$div.focus();
            return false;
        },
        'removeformat': function () {
            document.execCommand('RemoveFormat', false, true);
            document.execCommand('FormatBlock', false, '<p>');
            this.$div.focus();
            return false;
        }
    },

    translations: {
        'en':{
            'toolbar.bold': 'Bold',
            'toolbar.italic': 'Italic',
            'toolbar.strike': 'Strike',
            'toolbar.underline': 'Underline',
            'toolbar.left': 'Align Left',
            'toolbar.center': 'Align Center',
            'toolbar.right': 'Align Right',
            'toolbar.ol': 'Ordered List',
            'toolbar.ul': 'Unordered List',
            'toolbar.h1': 'Headline 1',
            'toolbar.h2': 'Headline 2',
            'toolbar.h3': 'Headline 3',
            'toolbar.image': 'Image',
            'toolbar.link': 'Link',
            'toolbar.video': 'Video',
            'toolbar.undo': 'Undo',
            'toolbar.redo': 'Redo',
            'toolbar.removeformat': 'Remove Format',

            'toolbar.html_mode': 'Switch to HTML Mode',
            'toolbar.visual_mode': 'Switch to Visual Mode',

            'modal.insert': 'Insert',
            'modal.cancel': 'Cancel',
            'modal.insert_image': 'Image',
            'modal.insert_video': 'Video',
            'modal.insert_link': 'Link',
            'modal.image': 'Image',
            'modal.link': 'Link',
            'modal.or': 'or',
            'modal.name': 'Name',
            'modal.html_code': 'HTML code'
        },
        'ru':{
            'toolbar.bold': 'Жирный',
            'toolbar.italic': 'Курсив',
            'toolbar.strike': 'Зачеркнутый',
            'toolbar.underline': 'Подчеркивание',
            'toolbar.left': 'Слева',
            'toolbar.center': 'По центру',
            'toolbar.right': 'Справа',
            'toolbar.ol': 'Нумерованый список',
            'toolbar.ul': 'Ненумерованный список',
            'toolbar.h1': 'Заголовок 1',
            'toolbar.h2': 'Заголовок 2',
            'toolbar.h3': 'Заголовок 3',
            'toolbar.image': 'Изображение',
            'toolbar.link': 'Ссылка',
            'toolbar.video': 'Видео',
            'toolbar.undo': 'Отмена',
            'toolbar.redo': 'Повтор',
            'toolbar.removeformat': 'Очистить форматирование',

            'toolbar.html_mode': 'Переключить в режим HTML',
            'toolbar.visual_mode': 'Переключить в визуальный режим',

            'modal.insert': 'Вставить',
            'modal.cancel': 'Отмена',
            'modal.insert_image': 'Вставка изображения',
            'modal.insert_video': 'Вставка видео',
            'modal.insert_link': 'Вставка ссылки',
            'modal.image': 'Изображение',
            'modal.link': 'Ссылка',
            'modal.or': 'или',
            'modal.name': 'Название',
            'modal.html_code': 'HTML код'
        }
    },

    tr: function (name) {
        return this.translations[this.language][name] ||  this.translations[this.default_language][name]
    },

    addToolbarButton: function (name) {
        var btn = $('<li><a class="pencil_toolbar_button pencil_toolbar_button__' + name + '" href="#" title="' + this.tr('toolbar.'+name) + '"></a></li>');
        this.getToolbar().append(btn);

    },

    addPlugin: function(name, func){
        this.toolbarButtons.push(name);
        this.plugins[name] = func;
    },

    getToolbar: function () {
        return $('.pencil_toolbar', this.$wrapper);
    },

    getButton: function (name) {
        return $('.pencil_toolbar_button__' + name, this.$wrapper);
    },

    getTemplate: function (name) {
        var html = this.templates[name];
        var context = this.translations[this.language];
        return this.renderTemplate(html, context);
    },

    renderTemplate: function (html, context){
        var tokens = html.match(/{{[\w\._]+}}/g) || [];
        for (var i=0; i<tokens.length; ++i){
            var token = tokens[i];
            var name = token.slice(2,-2);
            html = html.replace(token, context[name]);
        }
        return html;
    },

    insertHtml: function (html) {
        document.execCommand('InsertHtml', false, html);
    },

    visualMode: function () {
        if (this.mode === 'visual') {
            return;
        }
        this.$div.html(this.$textarea.val());
        this.$textarea.hide();
        this.$div.show();
        $('.pencil_switch_visual', this.$wrapper).hide();
        $('.pencil_switch_html', this.$wrapper).show();
        $('.pencil_toolbar', this.$wrapper).show();

        this.mode = 'visual';
    },
    htmlMode: function () {
        if (this.mode === 'html') {
            return;
        }
        this.$textarea.val(this.$div.html());
        this.$textarea.show();
        this.$div.hide();
        $('.pencil_switch_html', this.$wrapper).hide();
        $('.pencil_switch_visual', this.$wrapper).show();
        $('.pencil_toolbar', this.$wrapper).hide();

        this.mode = 'html';
    },
    showModal: function (templateName) {
        var bg = $(this.getTemplate('modal-background'));
        var modal = $(this.getTemplate('modal'));

        $('body').append(bg);
        $('body').append(modal);
        var content = this.getTemplate(templateName);
        modal.append(content);

        var left = $(window).width() / 2 - modal.width() / 2;
        var top = $(window).height() / 2 - modal.height() / 2;
        modal.css('left', left);
        modal.css('top', top);

        var _this = this;
        $('.pencil_modal_close,.pencil_modal_cancel').click(function () {
            _this.closeModal();
        });
        $(document).keyup(function (e) {
            if (e.keyCode === 27) {
                _this.closeModal();
            }
        });
    },
    closeModal: function () {
        $('.pencil_modal').remove();
        $('.pencil_modal_background').remove();
    },
    getSelectionStartNode: function () {
        //http://stackoverflow.com/questions/2459180/how-to-edit-a-link-within-a-contenteditable-div
        var node, selection;
        if (window.getSelection) { // FF3.6, Safari4, Chrome5 (DOM Standards)
            selection = window.getSelection();
            node = selection.anchorNode;
        }
        if (!node && document.selection) { // IE
            selection = document.selection;
            var range = selection.getRangeAt ? selection.getRangeAt(0) : selection.createRange();
            node = (range.commonAncestorContainer || range.parentElement) ? range.parentElement() : range.item(0);
        }
        if (node) {
            return (node.nodeName === "#text" ? node.parentNode : node);
        }
    },
    getSelectedText: function () {
        // http://stackoverflow.com/questions/5669448/get-selected-texts-html-in-div
        if (typeof window.getSelection !== "undefined") {
            // IE 9 and other non-IE browsers
            return window.getSelection().toString();
        }
        if (document.selection && document.selection.type !== "Control") {
            // IE 8 and below
            return document.selection;
        }
    },
    saveSelection: function () {
        //http://stackoverflow.com/questions/1181700/set-cursor-position-on-contenteditable-div
        if (window.getSelection) {
            //non IE Browsers
            this.savedRange = window.getSelection().getRangeAt(0);
        } else if (document.selection) {
            //IE
            this.savedRange = document.selection.createRange();
        }
    },
    restoreSelection: function () {
        //http://stackoverflow.com/questions/1181700/set-cursor-position-on-contenteditable-div
        this.$div.focus();
        if (this.savedRange !== null) {
            if (window.getSelection) {
                //non IE and there is already a selection
                var s = window.getSelection();
                if (s.rangeCount > 0) {
                    s.removeAllRanges();
                }
                s.addRange(this.savedRange);
            } else if (document.createRange) {
                //non IE and no selection
                window.getSelection().addRange(this.savedRange);
            } else if (document.selection) {
                //IE
                this.savedRange.select();
            }
        }
    },
    templates: {
        'toolbar': '<ul class="pencil_toolbar">\
            </ul>\
            <div style="clear: left;"></div>',

        'switch': '<div class="pencil_switch">\
                <a class="pencil_switch_html" href="#">{{toolbar.html_mode}}</a>\
                <a class="pencil_switch_visual" href="#">{{toolbar.visual_mode}}</a>\
            </div>',

        'modal': '<div class="pencil_modal"><div class="pencil_modal_close"></div></div>',

        'modal-background': '<div class="pencil_modal_background"></div>',

        'image-form': '<h1>{{modal.insert_image}}</h1>\
            <form class="pancil_modal_img_form" action="{{UPLOADER_URL}}" method="POST" enctype="multipart/form-data" >\
                <table>\
                    <tr>\
                        <td>{{modal.image}}:</td>\
                        <td>\
                            <input type="file" name="file" /><br />\
                        </td>\
                    </tr>\
                    <tr>\
                        <td><small>{{modal.or}}</small></td>\
                        <td></td>\
                    </tr>\
                    <tr>\
                        <td>{{modal.link}}:</td>\
                        <td><input type="text" name="url" size="40" value="" /></td>\
                    </tr>\
                    <tr colspan="2">\
                        <td>\
                            <input type="button" value="{{modal.insert}}" class="pencil_modal_submit" />\
                            <input type="button" value="{{modal.cancel}}" class="pencil_modal_cancel" />\
                        </td>\
                    </tr>\
                </table>\
            </form> ',

        'link-form': '<h1>{{modal.insert_link}}</h1>\
            <table>\
                <tr>\
                    <td>{{modal.name}}:</td>\
                    <td><input type="text" name="name" size="40" /></td>\
                </tr>\
                <tr>\
                    <td>{{modal.link}}:</td>\
                    <td><input type="text" name="url" size="40" value="http://" /></td>\
                </tr>\
                <tr colspan="2">\
                    <td>\
                        <input type="button" value="{{modal.insert}}" class="pencil_modal_submit" />\
                        <input type="button" value="{{modal.cancel}}" class="pencil_modal_cancel" />\
                    </td>\
                </tr>\
            </table>',

        'video-form': '<h1>{{modal.insert_video}}</h1>\
            <table>\
                <tr>\
                    <td colspan="2">\
                        {{modal.html_code}}:<br>\
                        <textarea name="html_code" cols="70" rows="7" />\
                    </td>\
                </tr>\
                <tr colspan="2">\
                    <td>\
                        <input type="button" value="{{modal.insert}}" class="pencil_modal_submit" />\
                        <input type="button" value="{{modal.cancel}}" class="pencil_modal_cancel" />\
                    </td>\
                </tr>\
            </table>'
    }

};

(function ($) {
    "use strict";

    $.fn.pencil = function (options) {
        var editor = new Pencil(this, options);
        editor.visualMode();
        return editor;
    };
}(jQuery));
