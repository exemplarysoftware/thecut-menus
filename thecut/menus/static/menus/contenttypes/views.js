define(['underscore', 'backbone.marionette', 'contenttypes/models', 'contenttypes/collections'], function (_, Marionette, models, collections) {


    'use strict';


    var OptionView = Marionette.ItemView.extend({

        attributes: function () {
            var attrs = {'value': this.model.get('id')};
            if (this.options.selected) {
                attrs.selected = 'selected';
            }
            return attrs;
        },

        tagName: 'option',

        template: _.template('<%= name %>')

    });


    var ContentTypeOptionView = OptionView.extend({

        template: _.template('<%= verbose_name %>')

    });


    var SelectView =  Marionette.CollectionView.extend({

        childView: OptionView,

        childViewOptions: function (model) {
            var data = {};
            if (model.get('id') === this.selectedId) {
                data.selected = true;
            }
            return data;
        },

        initialize: function (options) {
            SelectView.__super__.initialize.call(this, options);
            this.enabled = options.enabled;
            this.selectedId = options.selectedId;
        },

        onRender: function () {
            if (!this.enabled) {
                this.$el.attr('disabled', 'disabled');
            }
        },

        tagName: 'select',

        triggers: {
            'change': 'selectChanged'
        }

    });


    var ContentObjectSelectView = SelectView.extend({

        initialize: function (options) {
            ContentObjectSelectView.__super__.initialize.call(this, options);

            var contentType = new models.ContentType({
                'id': options.contentTypeId
            });
            contentType.fetch({async: false});

            var objects = contentType.get('objects');
            this.collection = new collections.ContentObjectCollection(objects);
        },

        tagName: 'select name="contentObject"'

    });


    var ContentTypeSelectView =  SelectView.extend({

        collection: new collections.ContentTypeCollection(),

        childView: ContentTypeOptionView,

        initialize: function (options) {
            ContentTypeSelectView.__super__.initialize.call(this, options);
            if (!this.collection.length) {
                this.collection.fetch({async: false}); // TODO
            }
        },

        tagName: 'select name="contentType"'

    });


    return {
        'ContentObjectSelectView': ContentObjectSelectView,
        'ContentTypeSelectView': ContentTypeSelectView
    };


});
