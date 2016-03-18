;(function($){
	var toolbarSupport={
		'bold':{icon:'fa fa-bold',tip:'加粗(Ctrl+B)',keycode:66,ctrl:true},
		'italic':{icon:'fa fa-italic',tip:'斜体(Ctrl+I)',keycode:73,ctrl:true},
		'header':{icon:'fa fa-header',tip:'标题(Ctrl+H)',keycode:72,ctrl:true},
		'ul':{icon:'fa fa-list-ul',tip:'无序列表(Ctrl+U)',keycode:85,ctrl:true},
		'ol':{icon:'fa fa-list-ol',tip:'有序列表(Ctrl+O)',keycode:79,ctrl:true},
		'code':{icon:'fa fa-code',tip:'代码(Ctrl+K)',keycode:75,ctrl:true},
		'quote':{icon:'fa fa-quote-left',tip:'引用(Ctrl+Q)',keycode:81,ctrl:true},
		'link':{icon:'fa fa-link',tip:'连接(Ctrl+L)',keycode:76,ctrl:true},
		'img':{icon:'fa fa-picture-o',tip:'图片(Ctrl+G)',keycode:71,ctrl:true},
		/*'file':{icon:'fa fa-file-o',tip:'文件',keycode:'',ctrl:true},*/
		'indent':{icon:'fa fa-indent',tip:'缩进(Tab)',keycode:9,ctrl:false},
		'preview':{icon:'fa fa-eye',tip:'浏览',keycode:false,ctrl:false},
		'fullscreen':{icon:'fa fa-arrows-alt',tip:'全屏',keycode:false,ctrl:false}
	};

	var defaults={
		wrapperClass:'editor',
		toolbarClass:'editor-toolbar',
		toolBtnClass:'item',
		textareaId:'',
		textareaClass:'editor-textarea',
		textareaName:'body',
		textareaHeight:'300px',
		previewClass:'editor-preview',
		indent:'    ',
		tools:['bold','italic','header','ul','ol','code','quote','link','img','file','indent','preview','fullscreen']
	};

	var Editor=(function(){
		var Editor=function($el,options){
			var opts=$.extend(defaults,options||{});
			for(var i=0;i<opts.tools.length;i++){
				if(!toolbarSupport[opts.tools[i]])
					opts.tools.splice(i--,1);
			}
			//view
			$el.addClass(opts.wrapperClass);
			var $toolbar
				=this.$toolbar
				=$('<div></div>')
				.addClass(opts.toolbarClass)
				.appendTo($el);
			opts.tools.forEach(function(val,i){
				var btn=$('<div></div>')
						.attr('title',toolbarSupport[val].tip)
						.addClass(opts.toolBtnClass)
						.addClass(opts.toolbarClass+'-'+val)
						.append($('<i></i>').addClass(toolbarSupport[val].icon))
						.appendTo($toolbar)
						.on('click',function(){
							if(methods[val])
								methods[val]();
						});
			});
			var $textarea=this.$textarea
						=$('<textarea></textarea>')
						.attr('id',opts.textareaId)
						.addClass(opts.textareaClass)
						.attr('name',opts.textareaName)
						.css('height',opts.textareaHeight)
						.css('display','block')
						.appendTo($el);
			var $preview=this.$preview
						=$('<div></div>')
						.addClass(opts.previewClass)
						.css('height',opts.textareaHeight)
						.css('display','none')
						.appendTo($el);
			
			//hotkey
			$textarea.attr('data-ctrl','').on('keyup',function(e){
				if(e.keyCode==17)$textarea.attr('data-ctrl','');
			}).on('keydown',function(e){
				if(e.keyCode==17){
					$textarea.attr('data-ctrl','true');
					e.preventDefault();
					return;
				}
				var ctrl=!!$textarea.attr('data-ctrl');
				opts.tools.forEach(function(val){
					var tool=toolbarSupport[val];
					if(tool.keycode==e.keyCode&&(!tool.ctrl||ctrl)){
						methods[val]();
						e.preventDefault();
					}
				});
			});

			var textarea=$textarea[0];
			var preview=$preview[0];

			//methods
			function get(el,entireRow){
				var text=
					// Mozilla Chrome IE9+
					('selectionStart' in el && function(){
						var val=el.value;
						//entire row
						if(entireRow===true){
							while(el.selectionStart>0&&val.charAt(el.selectionStart-1)!='\n'){
								el.selectionStart-=1;
							}
							while(el.selectionEnd<val.length&&val.charAt(el.selectionEnd)!='\n'){
								el.selectionEnd+=1;
							}
						}
						var len=el.selectionEnd - el.selectionStart;
						return val.substr(el.selectionStart,len);
					}()) || 
					// IE8-
					(document.selection && function(){
						el.focus();
						var r=document.selection.createRange();
						if(!r) return '';
						else return r.text;
					}()) || '';
				return text;
			}
			function replace(el,text,startOffset,endOffset,baseOnStart){
				var val = el.value;
				var result=
					//Mozilla Chrome IE9+
					('selectionStart' in el && function(){
						var start = el.selectionStart;
						var end = el.selectionEnd;
						var len = text.length;
						el.value = val.substr(0,start) + text + val.substr(end);
						if(startOffset===true || startOffset === undefined){
							el.selectionStart=start;
							el.selectionEnd=start+len;
						}else if(startOffset===false){
							el.selectionStart=el.selectionEnd=start+len;
						}else{
							el.selectionStart=start+startOffset;
							if(baseOnStart===true)
								el.selectionEnd=start+endOffset;
							else
								el.selectionEnd=start+len+endOffset;
						}
						el.focus();
						return true;
					}()) ||
					// IE8-
					(document.selection && function(){
						e.focus();
						document.selection.createRange().text=text;
						return true;
					}()) || false;
			}
			function format(str){
				var args=arguments;
				var result=str;
				for(var i=1;i<args.length;i++){
					if(args[i]!=undefined){
						result=result.replace(new RegExp('({)'+i+'(})','g'),args[i]);
					}
				}
				return result;
			}
			var methods={
				bold:function(){
					var reg=/^\*\*[^\0]*\*\*$/m;
					var text=get(textarea);
					if(!reg.test(text))
						return replace(textarea,format('**{1}**',text||'文字'),2,-2);
					else
						return replace(textarea,text.split('**')[1]);
				},
				italic:function(){
					var reg=/^_[^\0]*_$/m;
					var text=get(textarea);
					if(!reg.test(text))
						return replace(textarea,format('_{1}_',text||'文字'),1,-1);
					else
						return replace(textarea,text.split('_')[1]);
				},
				header:function(){
					var reg=/^#{1,6}\s[^\0]*/m;
					var text=get(textarea);
					if(!reg.test(text))
						return replace(textarea,format('### {1}',text||'标题'),4,0);
					else
						return replace(textarea,text.split(/#{1,6}\s/)[1]);
				},
				ul:function(){
					var reg=/^-\s/;
					var text=get(textarea,true);
					if(!reg.test(text))
						return replace(textarea,(text||'列表').split('\n').map(function(line){return '- '+line;}).join('\n'));
					else
						return replace(textarea,text.replace(/^-\s/gm,''));
				},
				ol:function(){
					var reg=/^\d+\.\s/;
					var text=get(textarea,true);
					if(!reg.test(text))
						return replace(textarea,(text||'列表').split('\n').map(function(line,index){return (index+1)+'. '+line}).join('\n'));
					else
						return replace(textarea,text.replace(/^\d+\.\s/gm,''));
				},
				code:function(){
					var reg=/^```[^\0]*```$/m;
					var text=get(textarea,true);
					if(!reg.test(text))
						return replace(textarea,format('```语言\n{1}\n```',text),3,5,true);
					else 
						return replace(textarea,text.split('```')[1]);
				},
				quote:function(){
					var reg=/^\>\s/;
					var text=get(textarea,true);
					if(!reg.test(text))
						return replace(textarea,(text||'引用').split('\n').map(function(line){return '> '+line;}).join('\n'));
					else
						return replace(textarea,text.replace(/^\>\s/gm,''));
				},
				link:function(){
					var reg=/^\[[^\0]*\]\([^\0]*\)$/m;
					var text=get(textarea)||'描述';
					if(!reg.test(text)){
						var url=prompt('链接地址：');
						if(!url)return false;
						else return replace(textarea,format('[{1}]({2})',text,url),1,1+text.length,true);
					}
					else return replace(textarea,text.split('[')[1].split(']')[0]);
				},
				img:function(){
					var reg=/^!\[[^\0]*\]\([^\0]*\)$/m;
					var text=get(textarea)||'描述';
					if(!reg.test(text)){
						var url=prompt('图片地址：');
						if(!url)return false;
						else return replace(textarea,format('![{1}]({2})',text,url),2,2+text.length,true);
					}
					else return replace(textarea,text.split('![')[1].split(']')[0]);
				},
				indent:function(){
					var text=get(textarea);
					if(!text)
						return replace(textarea,'    ',false);
					else{
						text=get(textarea,true);
						return replace(textarea,text.split('\n').map(function(line){return opts.indent+line;}).join('\n'));
					}
				},
				preview:function(){
					if($textarea.css('display')=='none'){
						$textarea.css('display','block');
						$preview.css('display','none');
					}else{
						$textarea.css('display','none');
						$preview.css('display','block');
						$preview.html(marked($textarea.val()));
						$preview.find('pre code').each(function(i,block){
							hljs.highlightBlock(block);
						});
					}
					return true;
				},
				fullscreen:function(){
					var el=$textarea.css('display')=='block'?textarea:preview;
					var rfs=el.requestFullScreen||
							el.webkitRequestFullScreen||
							el.mozRequestFullScreen;
					if(!rfs){
						alert('您的浏览器不支持全屏模式');
						return false;
					}else{
						rfs.call(el);
						return true;
					}
				}
			}
		}
		//Editor.prototype={}
		return Editor;
	})();

	$.fn.initEditor=function(options){
		return this.each(function(){
			var that=$(this);
			var editor=that.data('editor');
			if(!editor){
				editor=new Editor(that,options);
				that.data('editor',editor);
			}
		});
	}
})(jQuery);