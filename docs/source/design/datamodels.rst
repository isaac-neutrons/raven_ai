.. _datamodels:

DataModels
##########




DB Schema
+++++++++++++

.. mermaid::

 classDiagram

    Sample "1" -->"N" Environment
    Sample -->"N" Sample

    Sample "1" -->"1" Layer : substrate_layer
    Sample "1" -->"1<=N<=5" Layer : layers

    Layer "1" -->"1" Material : layer_material


    Measurement <|-- Reflectivity
    Measurement <|-- EIS

    Environment "1" -->"1" Material : ambiant_medium_material
    Environment "1" -->"N" Measurement

    Sample "1" -->"N" Publication 

    class Sample{
        +str description
        +list~Environment~ environments
        +Layer substrate
        +str geometry?
        +str main_composition
        +list~Layer~ layers
        +list~Publication~ publications
        +list ~Sample~ related_samples
    }


    class Layer{
        +Material material
        +float thickness
    }

    class Material{
        +str:composition
        +float mass?
        +float density?
    }
    
    class Measurement{
        +str lab        
        +str run_title
        +str run_number?
        +str proposal_number
        +enum facility
        +str probe
        +enum technique
        +str technique_description
        +bool is_simulated
        +datetime run_start
        +str raw_file_path
    }

    class Reflectivity{
        +float q_1_angstrom
        +float r
        +float d_r
        +float d_q
        +float measurement_geometry
        +datetime reduction_time
    }

    class EIS{
        +float frequency
        +float duration
        +float real_z
        +float imaginery_z
        +float phase
        +str potential

    }


    class Environment{
        +str description
        +Material ambiant_medium?
        +float temperature?
        +float pressure?
        +float relative_humidity?
        +list~Measurement~ measurements
        +datetime timestamp

    }


    class Publication{
        +str title
        +str url
        +str abstract
        +str notes
        +list~str~ keywords
    }

DataModel ODM vs BaseModel
+++++++++++++++++++++++++++

Classes defined as DataModel are stored in separate collections in the DB. Classes defined as (pydantic) BaseModel are embedded in the outter class's collections, e.g. JSON schema fields.



.. mermaid::

 classDiagram

    Sample <|-- DataModel
    Layer <|-- BaseModel
    Material <|-- BaseModel
    Measurement <|-- DataModel
    Environment <|-- DataModel
    Publication <|-- DataModel

    Sample --> Sample

    Sample "1" o-- "N" Environment
    Sample "1" *-- "1" Layer : substrate_layer
    Sample "1" *-- "1<=N<=5" Layer : layers

    Layer "1" *-- "1" Material : layer_material

    Measurement <|-- Reflectivity
    Measurement <|-- EIS

    Environment "1" *--"1" Material : ambiant_medium_material
    Environment "1" o--"N" Measurement

    Sample "N" o--"N" Publication     
    
    class Sample{
        +$get_foreign_key_fields(cls)
    }

    class Layer{

    }

    class Material{

    }
    
    class Measurement{

    }

    class Reflectivity{

    }

    class EIS{

    }

    class Environment{

        +$get_foreign_key_fields(cls)
    } 

    class DataModel{
        +str: Id
        +datetime: created_at
        +bool: is_deleted
        -$DBstore: _store
        
        +save(self, session)
        +delete(self,session)
        +restore(self,session)
        +view_object(self)

        +$connect_to_store(cls)
        +$find_by_id(cls, session, doc_id)
        +$find_active(cls, session)
        +$raw_rql(cls, session, query)
        +$get_foreign_key_fields(cls)
        +$validate_main_fields(cls, payload)
        +$get_foreign_key_fields(cls)
        +$validate_foreign_keys(cls,session, foreign_keys,field)
    }

    class BaseModel{

    } 
   
Considerations:

* Data Objects that are defined as *DataModel* (Sample, Measurement, Environment, Publication) are Documents within their DataModel-defined Collections. Relationships with other DataModel classes are defined as aggregation with the current schema. However, they can be deleted programmatically, if needed, in case there is a strong dependency with another DataModel object that needs to be deleted. 
* Data Objects that are defined as *BaseModel* (Layer, Material) by default introduce composition relationships with the associated DataModel classes. Thus layers, substrate and material are unique within the context they live, e.g. a material (ambiant_medium_material) for a specific environment only exists in that environment and no other DataModel object can point and refer to it. While materials with similar properties can exist on different environments, they are considered different (objects) with this schema. Additionally, if the main dataobject, e.g. environment, is deleted the associated BaseModel objects are deleted, too.
* The concepts of DataModel and BaseModel allow for the following:
    * BaseModel objects being embedded into the DataModel ones eliminate joins to retrieve them, while ensuring a standard format of the embedded objects.
    * DataModel Collections are to be used in the DB queries
    * BaseModel dataobjects cannot be queried directly
    * DataModel class enables for unified encapsulated operational and DB-wrapped capabilities


Note: We defined the relationships based on: UML composition models are nested documents with a dependent lifecycle, while aggregation models linked documents that can exist independently. Aggregation and composition are subsets of association.

Software Architecture
++++++++++++++++++++++++

Software Architecture

.. mermaid::

    architecture-beta
        group process(cloud)[WebApplication Process]
        group user(cloud)[api]

        service db(database)[Database]
        service WebServer(server)[WebServer] in process
        service MCPServer(server)[MCPServer] in process

        db:L -- R:WebServer

