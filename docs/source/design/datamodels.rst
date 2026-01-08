.. _datamodels:

DataModels
##########




DB Schema
+++++++++++++

.. mermaid::

 classDiagram

    Sample "1" -->"N" Environment
    Sample "1" -->"1" Substrate
    Sample "1" -->"1<=N<=5" Layer

    Substrate "1" -->"1" Material : substrate_material
    Layer "1" -->"1" Material : layer_material


    Measurement <|-- Reflectivity
    Measurement <|-- EIS

    Environment "1" -->"1" Material : ambiant_medium_material
    Environment "1" -->"N" Measurement

    Sample "1" -->"N" Publication 

    class Sample{
        +str description
        +list[Environment] environments
        +Substrate substrate
        +int main_layer_index
        +list[Layer] layers
        +list[Publication] publications
    }

    class Substrate{
        +Material material
        +str geometry?
        +float thickness?
    }

    class Layer{
        +Material material
        +float thickness
    }

    class Material{
        +str:composition
        +float mass?
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
        +dateTime run_start
        +str raw_file_path
    }

    class Reflectivity{
        +float q_1_angstrom
        +float r
        +float dR
        +float dQ
        +float measurement_geometry
        +dateTime reduction_time
    }

    class EIS{
        +float frequency
        +float real_z
        +float imaginery_z
        +float phase
        +str potential

    }


    class Environment{
        +str description
        +Material ambiant_medium?
        +float temperature?
        +float pressure
        +float relative_humidity?
        +list[Measurement] measurements
    
    }


    class Publication{
        +str title
        +str url
        +str abstract
        +str notes
        +list[str] keywords
    }

DataModel vs BaseModel
+++++++++++++++++++++++++

Classes defined as DataModel are stored in separate collections in the DB. Classes defined as (pydantic) BaseModel are embedded in the outter class's collections, e.g. JSON schema fields.



.. mermaid::

 classDiagram

    Sample "1" -->"N" Environment
    Sample "1" -->"1" Substrate
    Sample "1" -->"1<=N<=5" Layer

    Substrate "1" -->"1" Material : substrate_material
    Layer "1" -->"1" Material : layer_material


    Measurement <|-- Reflectivity
    Measurement <|-- EIS

    Environment "1" -->"1" Material : ambiant_medium_material
    Environment "1" -->"N" Measurement

    Sample "1" -->"N" Publication 


    Sample <|-- DataModel
    Layer <|-- BaseModel
    Substrate <|-- BaseModel
    Material <|-- BaseModel
    Measurement <|-- DataModel
    Environment <|-- DataModel
    Publication <|-- DataModel


   class DataModel{
        +str: Id
        +dateTime: created_at
        +bool: is_deleted
        -$DBstore: _store
        
        +save(self, session)
        +delete(self,session)
        +restore(self,session)

        +$connect_to_store(cls)
        +$find_by_id(cls, session, doc_id)
        +$find_active(cls, session)
        +$raw_rql(cls, session, query)
    }

    class BaseModel{

    }
    
    class Sample{

    }

    class Substrate{

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

    
    }


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


.. mermaid::

    block
        columns 3
        Frontend blockArrowId6<[" "]>(right) Backend
        space:2 down<[" "]>(down)
        Disk left<[" "]>(left) Database[("Database")]

        classDef front fill:#696,stroke:#333;
        classDef back fill:#969,stroke:#333;
        class Frontend front
        class Backend,Database back