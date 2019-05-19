$(document).ready(function () {
    var popupLoading = '<i class="notched circle loading icon green"></i>加载...';
    var ENTER_KEY = 13;
    var message_count = 0;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    socket.on('new message', function (data) {
        $('.messages').append(data.message_html);
        flask_moment_render_all();
        scrollToBottom();
        activateSemantics();
    });

    socket.on('user count', function (data) {
        $('#user-count').html(data.count);
    });

    socket.on('new message', function (data) {
        message_count++;
        if (!document.hasFocus()) {
            document.title = '(' + message_count + ')' + 'CatChat';
            if (data.user_id !== current_user_id) {
                messageNotify(data)
            }
        }
    });

    function scrollToBottom() {
        var $messages = $('.messages');
        $messages.scrollTop($messages[0].scrollHeight);
    }


    function new_message(e) {
        var $textarea = $('#message-textarea');
        var message_body = $textarea.val().trim();
        if (e.which === ENTER_KEY && !e.shiftKey && message_body) {
            e.preventDefault();
            socket.emit('new message', message_body);
            $textarea.val('');
        }
    }


    function load_messages() {
        var $messages = $('.messages');
        var position = $messages.scrollTop();
        var $msg = $('.msg-box');

        if (position === 0 && socket.nsp !== '/anonymous') {
            $('.ui.loader').toggleClass('active');
            $.ajax({
                url: messages_url,
                type: 'GET',
                data: {count: $msg.length},
                success: function (data) {
                    var before_height = $messages[0].scrollHeight;
                    $(data).prependTo('.messages').hide().fadeIn(800);
                    flask_moment_render_all();
                    $('.ui.loader').toggleClass('active');
                    activateSemantics();
                    var after_height = $messages[0].scrollHeight;
                    $messages.scrollTop(after_height - before_height);
                },
                error: function () {
                    alert('没有更多消息了.');
                    $('.ui.loader').toggleClass('active');
                }
            });
        }
    }

    function activateSemantics() {
        $('.ui.dropdown').dropdown();
        $('.ui.checkbox').checkbox();

        $('.message .close').on('click', function () {
            $(this).closest('.message').transition('fade');
        });

        $('#toggle-sidebar').on('click', function () {
            $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
        });

        $('#show-help-modal').on('click', function () {
            $('.ui.modal.help').modal({blurring: true}).modal('show');
        });

        $('#show-snippet-modal').on('click', function () {
            $('.ui.modal.snippet').modal({blurring: true}).modal('show');
        });

        $('.pop-card').popup({
            inline: true,
            on: 'hover',
            hoverable: true,
            html: popupLoading,
            delay: {
                show: 200,
                hide: 200
            },
            onShow: function () {
                var popup = this;
                popup.html(popupLoading);
                $.get({
                    url: $(popup).prev().data('href')
                }).done(function (data) {
                    popup.html(data);
                }).fail(function () {
                    popup.html('服务器错误, 请稍候重试.');
                });
            }
        });
    }

    function init() {

        document.addEventListener('DOMContentLoaded', function () {
            if (!Notification) {
                alert('你的浏览器不支持桌面提醒!');
                return;
            }
            if (Notification.permission !== 'granted') {
                Notification.requestPermission();
            }
        });

        $(window).focus(function () {
            message_count = 0;
            document.title = 'CatChat'
        });

        activateSemantics();
        scrollToBottom();
    }

    function messageNotify(data) {
        if (Notification.permission !== "granted") {
            Notification.requestPermission();
        } else {
            var notification = new Notification("消息来自" + data.nickname, {
                icon: data.gravatar,
                body: data.message_body.replace(/(<([^>]+)>)/ig, ""),
            });
            notification.onclick = function () {
                window.open(root_url);
            };
            setTimeout(function () {
                notification.close()
            }, 4000)
        }
    }

    $('#snippet-button').on('click', function () {
        var $snippet_textarea = $('#snippet-textarea');
        var message = $snippet_textarea.val();
        if (message.trim() !== '') {
            socket.emit('new message', message);
            $snippet_textarea.val('')
        }
    });

    $('.messages').scroll(load_messages);

    // submit message
    $('#message-textarea').on('keydown', new_message.bind(this));

    // open message modal on mobile
    $("#message-textarea").focus(function () {
        if (screen.width < 600) {
            $('#mobile-new-message-modal').modal('show');
            $('#mobile-message-textarea').focus()
        }
    });

    $('#send-button').on('click', function () {
        var $mobile_textarea = $('#mobile-message-textarea');
        var message = $mobile_textarea.val();
        if (message.trim() !== '') {
            socket.emit('new message', message);
            $mobile_textarea.val('')
        }
    });

    // quote message
    $('.quote-button').on('click', function () {
        var $textarea = $('#message-textarea');
        var message = $(this).parent().parent().parent().find('.message-body').text();
        $textarea.val('> ' + message + '\n\n');
        $textarea.val($textarea.val()).focus()
    });

    $('.delete-button').on('click', function () {
        var $this = $(this);
        if (!confirm('真的要删除吗?')) {
            return;
        }
        $.ajax({
            type: 'DELETE',
            url: $this.data('href'),
            success: function () {
                $this.parent().parent().parent().remove();
            },
            error: function () {
                alert('服务器错误')
            }
        });
    });

    $(document).on('click', '.delete-user-button', function () {
        var $this = $(this);
        if (!confirm('真的要删除吗?')) {
            return;
        }
        $.ajax({
            type: 'DELETE',
            url: $this.data('href'),
            success: function () {
                alert('用户被删除了');
                window.location.reload()
            },
            error: function () {
                alert('服务器错误')
            }
        });
    });

    init();

});
