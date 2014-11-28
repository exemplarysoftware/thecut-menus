define(

    ['jquery', 'jquery-ui', 'underscore', 'backbone.marionette',
        'menuitems/collections', 'menuitems/constants', 'contenttypes/views'],

    function ($, jQueryUi, _, Marionette, menuitemsCollections, constants,
        contenttypesViews) {


        'use strict';


        var sortableOptions = {
            'cursor': 'move',
            'handle': '.move.button',
            'update': function () {
                $.ajax({
                    'data': $(this).closest('.menu').sortable('serialize', {'key': 'pk', 'attribute': 'data-sortable-pk'}),
                    'error': function () {
                        alert('An error occured whilst processing this request.');
                    },
                    'type': 'POST',
                    'url': '/admin/menus/menuitem/api/menuitems/menuitem/' + $(this).closest('.menu').attr('data-pk') + '/reorder/'
                });
            }
        };


        var MenuItemCompositeView = Marionette.CompositeView.extend({

            addMenuItem: function (event) {
                var newItem = this.collection.add({'is_menu': false, 'title': 'New Item', 'parent': this.model.get('id')});
                event.stopPropagation();
                newItem.set('state', constants.states.EDIT);
            },

            addSubMenu: function (event) {
                var newMenu = this.collection.add({'is_menu': true, 'title': 'New group', 'parent': this.model.get('id')});
                event.stopPropagation();
                newMenu.set('state', constants.states.EDIT);
            },

            bindSortable: function () {
                this.$el.children('.menu').sortable(sortableOptions);
            },

            cancel: function (event) {
                this.model.set('state', constants.states.DISPLAY);
                // If this item hasn't been saved, delete it.
                if (!this.model.get('id')) {
                    this.model.destroy();
                }
                event.stopPropagation();
            },

            collection: new menuitemsCollections.MenuItemCollection(),

            childViewContainer: '@ui.itemList',

            destroyModel: function (event) {
                if (confirm('Are you sure you want to delete this item?')) {
                    this.model.destroy();
                }
                event.stopPropagation();
            },

            edit: function (event) {
                this.model.set('state', constants.states.EDIT);
                event.stopPropagation();
            },

            events: {
                'click @ui.addMenuItem': 'addMenuItem',
                'click @ui.addSubMenu': 'addSubMenu',
                'click @ui.delete': 'destroyModel',
                'click @ui.edit': 'edit',
                'click @ui.editCancel': 'cancel',
                'click @ui.editSave': 'save',
                'submit @ui.form': 'save'
            },

            fetchCollection: function () {
                if (this.model.get('id')) {
                    this.collection = new menuitemsCollections.MenuItemCollection([], {
                        'parentModel': this.model
                    });
                    this.collection.fetch();
                    this.on('render', this.bindSortable, this);
                }
            },

            initialize: function () {
                this.on('render', this.setAttributes, this);
                this.fetchCollection();
            },

            modelEvents: {
                'change': 'render debug',
                'change:id': 'fetchCollection'
            },

            debug: function (event) {
                console.log(event);
            },

            onRender: function () {
                if (this.model.get('state') === constants.states.EDIT) {
                    this.$el.find('input, select').first().focus();

                    if (!this.model.get('is_menu')) {
                        this.renderContentTypes();
                    }

                }
            },

            renderContentTypes: function () {
                var region = new Marionette.Region({'el': this.ui.contentTypeRegion});
                var contentTypeSelectView = new contenttypesViews.ContentTypeSelectView({
                    'enabled': this.model.get('state') === constants.states.EDIT,
                    'selectedId': this.model.get('content_type')
                });
                region.show(contentTypeSelectView);

                contentTypeSelectView.on('selectChanged', function () {
                    var contentTypeId = parseInt(this.ui.contentTypeRegion.find('[name="contentType"]').val(), 10);
                    this.renderContentObjects(contentTypeId);
                }, this);
                contentTypeSelectView.trigger('selectChanged');
            },

            renderContentObjects: function (contentTypeId) {
                var viewOptions = {
                    'enabled': this.model.get('state') === constants.states.EDIT,
                    'contentTypeId': contentTypeId
                };

                // If the content type matches the saved content type, then select the saved object
                if (contentTypeId === this.model.get('content_type')) {
                    viewOptions.selectedId = this.model.get('object_id');
                }

                var region = new Marionette.Region({'el': this.ui.contentObjectRegion});
                var ContentObjectSelectView = new contenttypesViews.ContentObjectSelectView(viewOptions);
                region.show(ContentObjectSelectView);
            },

            save: function (event) {
                this.model.save({
                    'title': this.ui.title.val().trim(),
                    'content_type': parseInt(this.ui.contentTypeRegion.find('[name="contentType"]').val(), 10) || null,
                    'object_id': parseInt(this.ui.contentObjectRegion.find('[name="contentObject"]').val(), 10) || null,
                    'state': constants.states.DISPLAY
                });
                this.bindUIElements();
                event.stopPropagation();
            },

            serializeData: function () {
                var data = MenuItemCompositeView.__super__.serializeData.call(this);
                return _.extend(data, {
                    'states': constants.states
                });
            },

            setAttributes: function () {
                this.$el.attr('data-pk', this.model.get('id'));
                this.$el.attr('data-sortable-pk', 'pk_' + this.model.get('id'));
            },

            tagName: 'li',

            template: Marionette.TemplateCache.get('script[type="text/template"][data-name="menuItem"]'),

            ui: {
                'addMenuItem': '[data-action="addMenuItem"]',
                'addSubMenu': '[data-action="addSubMenu"]',
                'contentTypeRegion': '[data-region="contentType"]',
                'contentObjectRegion': '[data-region="contentObject"]',
                'delete': '[data-action="delete"]',
                'edit': '[data-action="edit"]',
                'editCancel': '[data-action="editCancel"]',
                'editSave': '[data-action="editSave"]',
                'form': 'form',
                'itemList': 'ol',
                'title': '[name="title"]'
            }

        });


        return {
            'MenuItemCompositeView': MenuItemCompositeView
        };

    }

);
