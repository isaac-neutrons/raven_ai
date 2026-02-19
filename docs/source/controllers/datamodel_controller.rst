DataModel APIs
================

Routes and Controllers
------------------------

APIs correspond to the following data collections ({datamodel}) with field names and types as described in the corresponding class:

   - sample:
         .. autoclass:: models.sample.Sample
   - environment: 
      .. autoclass:: models.environment.Environment
   - reflectivity:
      .. autoclass:: models.measurement.Reflectivity
   - eis:
      .. autoclass:: models.measurement.EIS
   - publication:
      .. autoclass:: models.publication.Publication

The following  APIs cover basic operations for creating, updating, returning and deleting a document:

   - POST /{datamodel}/create
      .. autofunction:: controllers.datamodel_controller.create_dataobject
   
      e.g. ``http://0.0.0.0:3000/api/sample/create``

      Input POST (BODY)
      
      .. code-block:: json

         {   
         "description":"this is a test",
         "environment_ids":["88720291-5d4a-4f77-8319-03df6fe88fab"],
         "main_composition":"asffdaf",
         "substrate":
         {
               "material":{
                  "composition": "composition1",
                  "mass": 1.9,
                  "density":2.21
               },
               "thickness":1.2
         },
         "layers":[
               {
                  "material":{
                     "mass": 1.9,
                     "density":2.21,
                     "composition":"fsdf"
                  },
                  "thickness":1.2
               }
         ]
         }

      Output
      
      .. code-block:: json

         {
            "Id": "3c901c85-3235-41be-8984-2738253365ae",
            "description": "this is a test",
            "environment_ids": [
               "88720291-5d4a-4f77-8319-03df6fe88fab"
            ],
            "substrate": {
               "material": {
                     "composition": "composition1",
                     "mass": 1.9,
                     "density": 2.21
               },
               "thickness": 1.2
            },
            "main_composition": "asffdaf",
            "geometry": null,
            "layers": [
               {
                     "material": {
                        "composition": "fsdf",
                        "mass": 1.9,
                        "density": 2.21
                     },
                     "thickness": 1.2
               }
            ],
            "publication_ids": [],
            "related_sample_ids": []
         }

   - GET /{datamodel}/get/{obj_id}
      .. autofunction:: controllers.datamodel_controller.get_dataobject

      e.g. ``http://0.0.0.0:3000/api/eis/get/2bb8238e-f4b2-4729-9606-1cb1475daec7``

   
      Output
      
      .. code-block:: json

         {
            "Id": "2bb8238e-f4b2-4729-9606-1cb1475daec7",
            "proposal_number": "111111",
            "facility": "HFIR",
            "lab": "ORNL",
            "probe": "neutrons",
            "technique": "Reflectivity",
            "technique_description": "another",
            "is_simulated": true,
            "run_title": "Run34343",
            "run_number": "6",
            "run_start": "2024-05-19T11:30:00",
            "raw_file_path": "/home/user/file2.nxs",
            "frequency": 2.35,
            "duration": 10.65,
            "real_z": 5.66,
            "imaginery_z": 8.91,
            "phase": 6.65,
            "potential": "there is potential"
         }


   - POST /{datamodel}/update/{obj_id}
      .. autofunction:: controllers.datamodel_controller.update_dataobject

      e.g. ``http://0.0.0.0:3000/api/publication/update/6df8d543-b88f-44c3-9440-50b542c2c03e``

      Input POST (BODY)
      
      .. code-block:: json

         {
            "data":{
               "title": "Publication3",
               "url":"/home/usr/thsi/filee3.pdf",
               "abstract":" lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum\n lorem ipsum \n lorem ipsum 3.",
               "notes":"notes3 lorem ipsum lorem ipsum lorem ipsum lorem ",
               "keywords":["key3"]
            }
         }

      Output
      
      .. code-block:: json

         {
            "Id": "6df8d543-b88f-44c3-9440-50b542c2c03e",
            "title": "Publication3",
            "url": "/home/usr/thsi/filee3.pdf",
            "abstract":" lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum\n lorem ipsum \n lorem ipsum 3.",
            "notes":"notes3 lorem ipsum lorem ipsum lorem ipsum lorem ",
            "keywords": [
               "key3"
            ]
         }

   - DELETE /{datamodel}/delete/{obj_id}
      .. autofunction:: controllers.datamodel_controller.delete_dataobject
      
      e.g. ``http://0.0.0.0:3000/api/environment/delete/96a6cdf0-45a9-4a3f-8421-1d25b29b680e``

      Output
      
      .. code-block:: json

         {
            "status": "success",
            "deleted_id": "96a6cdf0-45a9-4a3f-8421-1d25b29b680e"
         }