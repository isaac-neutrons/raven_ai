from fastapi import Request
from models.sample import Sample,LayerData, MaterialData, SubstrateData
from models.environmentdata import EnvironmentData

async def home(request:Request):
    return {"message": "Welcome to Home"}

async def list_users(request: Request):
    print("request.state: ", request.state.__dict__)
    session = request.state.dbsession
    #users = list(session.query(object_type=dict))
    users=["u1","u2"]
    return users


async def create_sample(request: Request):

    material_0 = MaterialData(
        composition="composition1",
        mass=1.9
    )
    material_1 = MaterialData(
        composition="composition1",
        mass=1.6
    )
    material_2 = MaterialData(
        composition="composition2",
        mass=1.3
    )

    material_3 = MaterialData(
        composition="composition3",
        mass=1.99
    )
    
    environment_data = EnvironmentData(
        description="description",
        ambiant_medium= material_3,
        temperature=33,
        pressure=2.7,
        relative_humidity=12.90

    )
    saved_environment_data = await environment_data.save(request.state.dbsession)

    main_layer = LayerData(
        material=material_0,
        thickness=0.87
    )
    layers = [
        LayerData(
            material=material_1,
            thickness=0.99
        ), 
        LayerData(
        material=material_2,
        thickness=0.2
        )
    ]
    substrate = SubstrateData(
        material=material_0,
        dimensions={"x":0,"y":1,"z":3}
    )
    
    #create sample data object
    sample = Sample(
        description="sample data",
        environmentId= saved_environment_data.Id,
        substrate=substrate,
        main_layer= main_layer,
        layers=layers
    )
    saved_sample = await sample.save(request.state.dbsession)
    return saved_sample