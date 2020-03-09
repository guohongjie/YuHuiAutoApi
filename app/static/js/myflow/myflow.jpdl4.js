(function ($) {
    var myflow = $.myflow;
    $.extend(true, myflow.config.rect, {
        attr: {
            r: 8,
            fill: '#F6F7FF',
            stroke: '#03689A',
            "stroke-width": 2
        }
    });

//    $.extend(true, myflow.config.props.props, {
//        name: {
//            name: 'name', label: '名称', value: 'wctv', editor: function () {
////                return new myflow.editors.inputEditor();
//                return new myflow.editors.textEditor();;
//            }
//        },
//        globalkey: {
//            name: 'globalkey', label: '全局变量', value: '', editor: function () {
////                return new myflow.editors.inputEditor();
//                return new myflow.editors.textEditor();
//            }
//        }
//    });
    $.extend(true, myflow.config.tools.states, {
        start: {
            showType: 'image',
            type: 'start',
            name: {text: '<<start>>'},
            text: {text: '开始'},
            img: {src: 'static/img/flowImages/48/start.png', width: 48, height: 48},
            attr: {width: 48, height: 48},
            props: {
                show: {
                    name: 'show', label: '显示', value: '开始', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        start_active: {
            showType: 'image',
            type: 'start',
            name: {text: '<<start>>'},
            text: {text: '开始'},
            img: {src: 'static/img/flowImages/48/start_active.png', width: 48, height: 48},
            attr: {width: 48, height: 48},
            props: {
                show: {
                    name: 'show', label: '显示', value: '开始', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        start_mark: {
            showType: 'image',
            type: 'start',
            name: {text: '<<start>>'},
            text: {text: '开始'},
            img: {src: 'static/img/flowImages/48/start_mark.png', width: 48, height: 48},
            attr: {width: 48, height: 48},
            props: {
                show: {
                    name: 'show', label: '显示', value: '开始', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        end: {
            showType: 'image', type: 'end',
            name: {text: '<<end>>'},
            text: {text: '结束'},
            img: {src: 'static/img/flowImages/48/end.png', width: 48, height: 48},
            attr: {width: 48, height: 48},
            props: {
                show: {
                    name: 'show', label: '显示', value: '结束', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        end_active: {
            showType: 'image', type: 'end',
            name: {text: '<<end>>'},
            text: {text: '结束'},
            img: {src: 'static/img/flowImages/48/end_active.png', width: 48, height: 48},
            attr: {width: 48, height: 48},
            props: {
                show: {
                    name: 'show', label: '显示', value: '结束', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        end_mark: {
            showType: 'image', type: 'end',
            name: {text: '<<end>>'},
            text: {text: '结束'},
            img: {src: 'static/img/flowImages/48/end_mark.png', width: 48, height: 48},
            attr: {width: 48, height: 48},
            props: {
                show: {
                    name: 'show', label: '显示', value: '结束', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        error: {
            showType: 'image', type: 'error',
            name: {text: '<<error>>'},
            text: {text: '错误'},
            img: {src: 'static/img/flowImages/48/error.png', width: 24, height: 24},
            attr: {width: 24, height: 24},
            props: {
                show: {
                    name: 'show', label: '显示', value: '错误', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        error_active: {
            showType: 'image', type: 'error',
            name: {text: '<<error>>'},
            text: {text: '错误'},
            img: {src: 'static/img/flowImages/48/error_active.png', width: 24, height: 24},
            attr: {width: 24, height: 24},
            props: {
                show: {
                    name: 'show', label: '显示', value: '错误', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        error_mark: {
            showType: 'image', type: 'error',
            name: {text: '<<error>>'},
            text: {text: '错误'},
            img: {src: 'static/img/flowImages/48/error_mark.png', width: 24, height: 24},
            attr: {width: 24, height: 24},
            props: {
                show: {
                    name: 'show', label: '显示', value: '错误', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                }
            }
        },
        task: {
            showType: 'text', type: 'task',
            name: {text: '<<task>>'},
            text: {text: '任务'},
            attr: {width: 100, height: 50, fill: '#ffffff', stroke: "#353c48 ", r: 25},
            img: {src: 'static/img/flowImages/48/task_sql.png', width: 0, height: 0},
            props: {
                text: {
                    name: 'text', label: '显示', value: '任务', editor: function () {
                        return new myflow.editors.textEditor();
                    }
                },
                api_id: {
                    name: 'api_id', label: '接口ID', value: '::', editor: function () {
                        return new myflow.editors.inputEditor();
                    }
                },
                params: {
                    name: 'params', label: '参数', value: ':', editor: function () {
                        return new myflow.editors.inputEditor();
                    }
                },
//                localkey: {
//                    name: 'localkey', label: '回单变量', value: '', editor: function () {
//                        return new myflow.editors.inputEditor();
//                    }
////                },
//                transformationGlobal: {
//                    name: 'transformationGlobal', label: '转换全局', value: '', editor: function () {
//                        return new myflow.editors.inputEditor();
//                    }
//                }
            }
        },
        name: {
            name: 'name', label: '名称', value: 'wctv', editor: function () {
//                return new myflow.editors.inputEditor();
                return new myflow.editors.textEditor();;
            }
        },

    });
})(jQuery);