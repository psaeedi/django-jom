{% load jom_tags jom_filters %}/**{# JomEntry class skeleton rendered as a Django template #}
 * {{ clazz }}  class file
 * Generated on {% now 'DATETIME_FORMAT' %}
 * 
 * Please do not edit this file as it will be overridden.
 */{% block jom_def %}
{{ clazz }} = function(config) {
	/* Fields */
	this.fields = new Array();{% for name in fields.keys %}
	this.fields['{{ name }}'] = undefined;{% endfor %}
	
	// Foreign keys
	this.fk = new Array();
	
	// m2m keys
	this.m2m = new Array();
	
	this.init = function(config) {
		for(var key in config) {
			if (this.fields.hasOwnProperty(key)) {
				// Public fields have a setter.
				var setter = "set" + camel(key);
				if (this.fields.hasOwnProperty(setter)) {
	            	this[setter](config[key]);
				} else {
					this.fields[key] = config[key];
				}
			}
        }
	};
	this.init(config);
};

{% block save %}/**
 * Export to a data map.
 */
{{ clazz }}.prototype.toMap = function() {
	var json = {};
	json['model'] = '{{ model }}';
	for (var key in this.fields) {
		json[key] = this.fields[key];
	}
	
	for (var key in this.fk) {
		var fk = this.fk[key];
		if (fk != undefined) {
			// replace id with FK
			json[key] = fk.toMap();
		}
	}
	
	for (var key in this.m2m) {
		m2m[key] = this.m2m[key];
		var m2m = this.m2m[key];
		if (m2m != undefined) {
			// replace ids with m2m
			var m2mJson = new Array();
			for (m2mId in m2m) {
				m2mJson[key] = m2m.toMap();
			}
			json[key] = m2mJson;
		}
	}
	
	return json;
};

var {{ clazz|capital }}_ASYNC_SAVE_URL = '/jom/save/';

/**
 * Save the instance and all the loaded FK on the server.
 * 
 * @callback successCallback()
 * @callback errorCallback(message)
 */
{{ clazz }}.prototype.asyncSave = function(successCallback, errorCallback) {
	$.ajax({
    	url: {{ clazz|capital }}_ASYNC_SAVE_URL,
    	data: this.toMap(),
    	dataType: 'json',
    	type: 'POST',
    	traditional: true,
    	success: function(jsonResponse) { 
    		if (jsonResponse.result == true) {
    			successCallback()
    		} else {
    			errorCallback(jsonResponse.message)
    		}
    	},
    	error: function() { 
    		errorCallback("The server was unreachable.");
    	}
	});
};{% endblock %}

{% block jom_deg_accessor %}
{% for name, fieldJs in fields.items %}{{ fieldJs }}
{% endfor %}{% endblock %}{% block jom_def_extra %}{% endblock %}
{% endblock %}

{% block factory_def %}/**
* Define a {{ clazz }}Factory singleton factory class.
* 
* {{ clazz }}Factory can create or get {{ clazz }} instances.
*/
{{ clazz }}Factory = function() {
	this.joms = new Array();
};

{{ clazz }}Factory.prototype.get = function(instanceId) {
	return this.joms[instanceId];
};

{{ clazz }}Factory.prototype.getOrCreate = function(instanceId, fieldMap) {
	var jom =  this.joms[instanceId];
	if (jom == undefined) {
		jom = new {{ clazz }}({{% for name, fieldClass in fields.items %}
            '{{ name }}': fieldMap['{{ name }}']{% if not forloop.last %},{% endif %}{% endfor %}});
        this.joms[instanceId] = jom;
	}
	return jom;
};

/**
 * Asynchronously get an existing JomInstance from the server.
 * 
 * @param instanceId the id of the Jom to fetch
 * @callback successCallback(jomInstance)
 * @callback errorCallback(message)
 */
{{ clazz }}Factory.prototype.asynchGet = function(instanceId, successCallback, errorCallback) {
	var jom =  this.joms[instanceId];
	if (jom == undefined) {
		// TODO(msama): not implemented yet.
		throw "Not implemented yet";
	}
	return jom;
};

/**
 * Asynchronously create a new JomInstance on the server.
 * 
 * @callback successCallback(jomInstance)
 * @callback errorCallback(message)
 */
{{ clazz }}Factory.prototype.asynchCreate = function(successCallback, errorCallback) {
	// TODO(msama): not implemented yet.
	throw "Not implemented yet";
};

var singleton{{ clazz }}Factory = new {{ clazz }}Factory();
{% endblock %}