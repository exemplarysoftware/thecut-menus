define([
    'jquery',
    'jquery-ui',
    'underscore',
    'backbone',
    'contenttypes/collections',
    'contenttypes/models',
    'contenttypes/views',
    'menuitems/collections'
], function(
    $,
    jqueryUI,
    _,
    Backbone,
    contenttypesCollections,
    contenttypesModels,
    contenttypesViews,
    menuitemsCollections
) {


    var sortableOptions = {
        'cursor': 'move',
        'handle': '.move.button',
        'update': function(event, ui) {
            $.ajax({
                'data': $(this).closest('ul').sortable('serialize', {'key': 'pk', 'attribute': 'data-sortable-pk'}),
                'error': function(XMLHttpRequest, textStatus, errorThrown) {
                    alert('An error occured whilst processing this request.');
                },
                'type': 'POST',
                'url': '/admin/menus/menuitem/api/menuitems/menuitem/' + $(this).closest('ul').attr('data-pk') + '/reorder/',
            });
        },
    }


    var MenuItemView = Backbone.View.extend({

        // HTML & CSS attributes.
        template: _.template($("#menuitem-template").html()),
        tagName: 'li',
        className: 'menuitem',

        attributes: function() {
            return {
                'data-pk': this.model.get('id'),
                'data-sortable-pk': 'pk_' + this.model.get('id'),
            };
        },

        events: {
            'click .edit.button': 'editClicked',
            'click .save.button': 'saveClicked',
            'click .cancel.button': 'cancelClicked',
            'click .delete.button': 'destroy',
            'change select.contenttype': 'updateContentType',
            'change select.contentobject': 'updateContentObject',
        },


        render: function() {
            // Render the contents of this single MenuItem.
            this.$el.html(this.template(this.model.toJSON()));
            // Insert any children this MenuItem might have.
            if ( this.model.get('is_menu') ) {
                this.children = new MenuItemCollectionView({
                    'id': this.model.get('id')
                });
                this.children.render();
                this.$el.append(this.children.el);
            }
            return this;
        },

        save: function() {
            // Persist the changes made to the model.
            var titleValue = $(this.el).find("input.title").val().trim();
            this.model.save({title: titleValue});
        },

        destroy: function(event) {
            if (confirm("Are you sure you want to delete this item?")) {
              this.model.destroy();
            }
            event.stopPropagation();
        },

        // Custom functions.

        isEditable: function() {
            var saveButton = $(this.el).children('.form').find(".save.button");
            return saveButton.hasClass("enabled");
        },

        editClicked: function(event) {
            if ( this.model.get('state') == this.model.states.DISPLAY ) {
                this.allowEditing();   // TODO: listen to model change.
            }
            this.model.toggleState();
            event.stopPropagation();
        },

        saveClicked: function(event) {
            if ( this.model.get('state') == this.model.states.EDIT ) {
                this.save();
                this.preventEditing(); // TODO: listen to model change.
                this.render();
            }
            this.model.toggleState();
            event.stopPropagation();
        },

        cancelClicked: function(event) {
            this.model.toggleState();
            this.render();
            event.stopPropagation();
        },

        populateContentObjectSelect: function(contentTypes) {
            // Populate and enable the content object selector.
            var el = $(this.el).children('.form').find("select.contentobject");

            // The <select> for choosing the content object, won't exist
            // if this is a sub-menu.
            if ( el.length > 0 ) {
                el.empty();
                el.removeClass("disabled").addClass("enabled");
                el.prop("disabled", false);
                var contentType = new contenttypesModels.ContentType({id: this.model.get('content_type')});
                contentType.fetch({async: false});
                return contentType.getContentObjectSelect(el, this.model.get('object_id'));
            }
        },

        updateContentType: function(event) {
            // Update this item's content type and populate the content
            // object selector with items of the selected type.
            var el = $(this.el).children('.form').find('select.contenttype');

            // The <select> for choosing the content type, won't exist if
            // this is a sub-menu.
            if ( el.length > 0 ) {
                this.model.set({content_type: el.val()});
                var contentTypes = new contenttypesCollections.ContentTypeCollection();
                contentTypes.fetch({async: false});
                this.populateContentObjectSelect(contentTypes);
                this.updateContentObject();
            }
            event.stopPropagation();
        },

        updateContentObject: function() {
            var select = $(this.el).children('.form').find('select.contentobject');
            if ( select.length > 0) {
                this.model.set({object_id: parseInt(select.val(), 10)});
            }
        },

        allowEditing: function() {
            // Put the form into an editable state.

            // Make the 'title' field editable.
            var titleField = $(this.el).children('.form').find("input.title");
            titleField.removeClass("disabled").addClass("enabled");
            titleField.prop("disabled", false);

            // Enable labels
            var fieldLabel = $(this.el).children('.form').find("label");
            fieldLabel.removeClass("hidden");

            // Disable 'target' element
            var menuTarget = $(this.el).children('.form').find(".target");
            menuTarget.addClass("hidden");

            // Enable 'edit-controls' container
            var editControls = $(this.el).children('.form').find(".edit-controls");
            editControls.removeClass("hidden");

            // Disable the 'Edit' button.
            var editButton = $(this.el).children('.form').find(".edit.button");
            editButton.addClass("disabled").removeClass("enabled");

            // Disable the 'Delete' button.
            var deleteButton = $(this.el).children('.form').find(".delete.button");
            deleteButton.addClass("disabled").removeClass("enabled");

            // Populate and enable the content type selector.
            var selector = $(this.el).children('.form').find("select.contenttype");
            if ( selector.length > 0 ) {
                selector.empty();
                var contentTypes = new contenttypesCollections.ContentTypeCollection();
                var active = this.model.get('content_type');
                contentTypes.fetch({async: false});
                contentTypes.populateContentTypeSelect(selector, active);
                selector.removeClass("disabled").addClass("enabled");
                selector.prop("disabled", false);
                this.populateContentObjectSelect(contentTypes);
            }
        },

        preventEditing: function() {
            // Make the 'title' field non-editable.
            var titleField = $(this.el).children('.form').find("input.title");
            titleField.addClass("disabled").removeClass("enabled");
            titleField.prop("disabled", true);

            // Disable labels
            var fieldLabel = $(this.el).children('.form').find("label");
            fieldLabel.addClass("hidden");

            // Enable 'target' element
            var menuTarget = $(this.el).children('.form').find(".target");
            menuTarget.removeClass("hidden");

            // Disable 'edit-controls' container
            var editControls = $(this.el).children('.form').find(".edit-controls");
            editControls.addClass("hidden");

            // Enable the 'Edit' button.
            var editButton = $(this.el).children('.form').find(".edit.button");
            editButton.removeClass("disabled").addClass("enabled");

            // Enable the 'Delete' button.
            var deleteButton = $(this.el).children('.form').find(".delete.button");
            deleteButton.removeClass("disabled").addClass("enabled");

            // Disable the content type select.
            var contentTypeSelect = $(this.el).children('.form').find("select.contenttype");
            contentTypeSelect.addClass("disabled").removeClass("enabled");
            contentTypeSelect.prop("disabled", true);

            // Disable the content object select.
            var contentObjectSelect = $(this.el).children('.form').find("select.contentobject");
            contentObjectSelect.addClass("disabled").removeClass("enabled");
            contentObjectSelect.prop("disabled", true);
        },

    });


    var MenuItemCollectionView = Backbone.View.extend({

        tagName: 'div',
        template: _.template($("#menu-template").html()),
        className: 'menu',
        events: {
            'click .add.menuitem.button': 'addMenuItemButtonClicked',
            'click .add.menuitem .save.button': 'addMenuItemSaveClicked',
            'click .add.menuitem .cancel.button': 'addMenuItemCancelClicked',
            'change .add.menuitem select.contenttype': 'contentTypeChanged',
            'click .add.submenu.button': 'addSubMenuButtonClicked',
            'click .add.submenu .save.button': 'addSubMenuSaveClicked',
            'click .add.submenu .cancel.button': 'addSubMenuCancelClicked',
        },

        initialize: function() {
            this.collection = new menuitemsCollections.MenuItemCollection(this.id);
            this.listenTo(this.collection, 'destroy', this.menuItemDestroyed);
        },

        render: function() {
            // Render the containing template.
            this.$el.html(this.template({id: this.id}));

            // Render the list of menu items inside this collection.
            var list = this.$el.find("ul.menu");
            this.collection.fetch({async: false});
            this.collection.each(function(menuitem) {
                var itemView = new MenuItemView({model: menuitem});
                list.append(itemView.render().el);
            }, this);

            // Render a <select> element for the Content Types.
            var select = this.$el.find('li.menuitem.add select.contenttype');
            var contentTypeSelect = new contenttypesViews.ContentTypeCollectionView({
                el: select, contentTypeId: null});
            contentTypeSelect.render();

            // Render a <select> element for the Content Type's Content Objects.
            var selectedContentType = new contenttypesModels.ContentType({id: select.val()});
            this.renderContentObjectSelect(selectedContentType);

            // Bind jQuery UI sortable to the menut items in this collection.
            this.$el.children('ul.menu').sortable(sortableOptions);

            return this;
        },

        addSubMenuButtonClicked: function(event) {
            var form = $(this.el).children('ul.controls')
                .children('li.add.submenu').find('div.form').removeClass('hidden');
            event.stopPropagation();
            return false;
        },

        // Save the new sub menu to the server.
        addSubMenuSaveClicked: function(event) {
            var title = $(this.el).children('ul.controls')
                .children('li.add.submenu').find('input.title').val();
            this.collection.create({'title': title,
                                    'parent': this.collection.parentId});
            this.render();
            event.stopPropagation();
            return false;
        },

        // Cancel adding a new sub menu.
        addSubMenuCancelClicked: function(event) {
            var form = $(this.el).children('ul.controls')
                .children('li.add.submenu').find('div.form');
            form.addClass('hidden');
            form.find('input.title').val('');

            event.stopPropagation();
            return false;
        },

        addMenuItemButtonClicked: function(event) {
            var form = $(this.el).children('ul.controls')
                .children('li.add.menuitem').find('div.form').removeClass('hidden');

            event.stopPropagation();
            return false;
        },

        addMenuItemSaveClicked: function(event) {
            var title = $(this.el).children('ul.controls')
                .children('li.add.menuitem').find('input.title').val();
            var contentType = this.$el.find('li.add.menuitem select.contenttype').val();
            var contentObject = this.$el.find('li.add.menuitem select.contentobject').val();
            this.collection.create({'title': title, 'content_type': contentType,
                                    'object_id': contentObject,
                                    'parent': this.collection.parentId});
            this.render();
            // Prevent the event from propagating and firing multiple times. For
            // some reason event.stopPropagation() does not work
            // here. JavaScript. See https://stackoverflow.com/questions/10522562/
            event.stopPropagation();
            return false;
        },

        addMenuItemCancelClicked: function(event) {
            // Render this view again which will hide the "form" used to add new
            // menu items. NB: may need to just add/remove class here if the page
            // flicker is deemed unbearable when re-rendering.
            this.render();
            event.stopPropagation();
            return false;
        },

        contentTypeChanged: function() {
            var selected = this.$el.find('li.add.menuitem select.contenttype').val();
            var contentType = new contenttypesModels.ContentType({id: selected});
            this.renderContentObjectSelect(contentType);
        },

        // Render a <select> element which allows selection of a Content Object for
        // the given Content Type.
        renderContentObjectSelect: function(contentType) {
            contentType.fetch({async: false});
            var objects = contentType.get('objects');
            var contentObjectCollection = new contenttypesCollections.ContentObjectCollection(objects);
            var contentObjectSelect = this.$el.find('li.add.menuitem select.contentobject');
            var contentObjectView = new contenttypesViews.ContentObjectView({
                collection: contentObjectCollection,
                el: contentObjectSelect,
            });
            contentObjectView.render();
        },

        menuItemDestroyed: function() {
            this.render();
        }

    });


    // The "application" view, which sets up and renders the initial
    // content.
    var MenuView = Backbone.View.extend({

        el: '#menu',

        render: function() {
            // Create and render the root-level menu. This will in turn
            // create and render it's own child menus.
            var pk = this.$el.attr("data-pk" || null);
            this.rootMenu = new MenuItemCollectionView({id: pk});
            this.$el.html(this.rootMenu.render().el);
        }

    });


    return {
        'MenuItemCollectionView': MenuItemCollectionView,
        'MenuItemView': MenuItemView,
        'MenuView': MenuView
    };

});
