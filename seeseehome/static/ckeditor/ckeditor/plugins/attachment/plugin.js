CKEDITOR.plugins.add( 'attachment', {
    icons: 'attachment',
    listId: 'attachment-list',
    init: function( editor ) {
        // Plugin logic goes here...

        editor.ui.addButton( 'attachment', {
			label: 'attachment',
			command: 'attachment',
			toolbar: 'insert'
		});

		// editor.addCommand( 'attachment', {
	 //        exec: function( editor ) {
	 //            // alert( 'Executing a command for the editor name "' + editor.name + '"!' );
	 //            var attach_list_id = editor.config.attach_list_id ? editor.config.attach_list_id : "attachment-list";
	 //            var attach_list = $(document.getElementById(attach_list_id));
	 //            var files_input = $('<input type="file" name="attachment_files" multiple>');
	 //            var form = $('<form></form>').append(files_input);
	 //            $('body').append(form);
	 //            files_input.change(function() {
		// 			// console.log(files_input.val().split('\\').pop())
		// 			console.log(files_input.val());
		// 		});

	 //            files_input.click();

		// 	}
	 //    });

	    CKEDITOR.on('instanceReady', function(event) {
			var uploader = new plupload.Uploader({
				runtimes : 'html5,flash,silverlight,html4',
				browse_button : editor.ui.instances.attachment._.id, // you can pass in id...
				// container: document.getElementById('container'), // ... or DOM Element itself
				url : './',
				flash_swf_url : '../js/Moxie.swf',
				silverlight_xap_url : '../js/Moxie.xap',
				filters: ATTACH_FILTERS,
				// filters : {
					// max_file_size : '10mb',
					// mime_types: [
					// 	{title : "Image files", extensions : "jpg,gif,png"},
					// 	{title : "Zip files", extensions : "zip"}
					// ]
				// },

				init: {
					PostInit: function() {
						if(CKEDITOR.editor.attachInit)
							CKEDITOR.editor.attachInit();
					},
					FilesAdded: function(up, files) {
						if(CKEDITOR.editor.attachFileAdded)
							CKEDITOR.editor.attachFileAdded(up, files);
					},
					FileUploaded: function(up, file, ret) {
						if(CKEDITOR.editor.attachFileUploaded)
							CKEDITOR.editor.attachFileUploaded(up, file, ret);
					},
					UploadComplete: function() {
						if(CKEDITOR.editor.attachUploaded)
							CKEDITOR.editor.attachUploaded();
					},
					UploadProgress: function(up, file) {
						if(CKEDITOR.editor.attachUploading)
							CKEDITOR.editor.attachUploading(up, file);
					},
					BeforeUpload: function(up, file) {
						if(CKEDITOR.editor.attachBeforeUpload)
							CKEDITOR.editor.attachBeforeUpload(up, file);
					},
					Error: function(up, err) {
						if(CKEDITOR.editor.attachError)
							CKEDITOR.editor.attachError(up, err);
					}
				}
			});
			CKEDITOR.editor.uploader = uploader;
			uploader.init();
	    });
    }
});