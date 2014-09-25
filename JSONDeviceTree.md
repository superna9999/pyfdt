## JSON Flattened Device Tree Format ##
----------
pyfdt can output and import JSON formatted Flattedned Device Tree.

The structure is :

    {
	    nodes, nodes
	}

nodes :

	"node-name" : {
		properties,
		nodes
	}

properties :

	"property-name" : property-value

properties value :

 - strings

	["strings", "string1",..."laststring"]

 - words

	["words", "0x01abcdef",..."0x00000000"]

 - bytes
 
	["bytes", "12", "1f", "-64", ..., "0"]

 - without value
	
	null

A complete example :

	{
		"compatible": ["strings", "my,model"],
		"memory": {
			"device_type": ["strings", "memory"],
			"reg": ["words", "0x00000000", "0x00000000"],
			"cfg": ["bytes", "12", "23", "-64"]
		},
		"chosen" : {
			"cmdline": ["strings", "debug=on"]
		}
	}
