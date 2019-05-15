$(document).ready(function () {
    // login form
    $('.login.ui.form')
        .form({
            fields: {
                email: {
                    identifier: 'email',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入Email地址'
                        },
                        {
                            type: 'email',
                            prompt: '请输入正确的Email地址'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入密码'
                        },
                        {
                            type: 'minLength[8]',
                            prompt: '密码长度不得少于{ruleValue}个字符'
                        }
                    ]
                }
            }
        });

    // register form
    $('.register.ui.form')
        .form({
            inline: true,
            fields: {
                nickname: {
                    identifier: 'nickname',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入你的昵称'
                        },
                        {
                            type: 'maxLength[30]',
                            prompt: '昵称长度不得超过{ruleValue}个字符'
                        }
                    ]
                },
                email: {
                    identifier: 'email',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入Email地址'
                        },
                        {
                            type: 'email',
                            prompt: '请输入正确的Email地址'
                        }
                    ]
                },
                password: {
                    identifier: 'password',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入密码'
                        },
                        {
                            type: 'minLength[8]',
                            prompt: '密码长度不得少于{ruleValue}个字符'
                        }
                    ]
                },
                password2: {
                    identifier: 'password2',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入密码'
                        },
                        {
                            type: 'minLength[8]',
                            prompt: '密码长度不得少于{ruleValue}个字符'
                        },
                        {
                            type: 'match[password]',
                            prompt: '两次输入的密码不一致'
                        }
                    ]
                },
                terms: {
                    identifier: 'terms',
                    rules: [
                        {
                            type: 'checked',
                            prompt: '你必须同意条款才能继续'
                        }
                    ]
                }
            }
        });

    // profile form
    $('.profile.ui.form')
        .form({
            inline: true,
            fields: {
                nickname: {
                    identifier: 'nickname',
                    rules: [
                        {
                            type: 'empty',
                            prompt: '请输入你的昵称'
                        },
                        {
                            type: 'maxLength[30]',
                            prompt: '昵称长度不得超过{ruleValue}个字符'
                        }
                    ]
                },
                github: {
                    identifier: 'github',
                    optional: true,
                    rules: [
                        {
                            type: 'url',
                            prompt: '请输入正确的网址'
                        }
                    ]
                },
                website: {
                    identifier: 'website',
                    optional: true,
                    rules: [
                        {
                            type: 'url',
                            prompt: '请输入正确的网址'
                        }
                    ]
                },
                bio: {
                    identifier: 'bio',
                    optional: true,
                    rules: [
                        {
                            type: 'maxLength[120]',
                            prompt: '自我介绍不得超过120个字'
                        }
                    ]
                }
            }
        });
});
