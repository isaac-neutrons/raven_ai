from fastapi import Request
from models.sample import Sample,Layer, Material, Substrate
from models.environment import Environment

async def home(request:Request):
    return {"message": "Welcome to Home"}

async def list_users(request: Request):
    print("request.state: ", request.state.__dict__)
    session = request.state.dbsession
    #users = list(session.query(object_type=dict))
    users=["u1","u2"]
    return users


async def delete_sample(request:Request):
    session = request.state.dbsession
    #sample=session.load("samples/610-A", object_type=Sample)
    sample = await Sample.find_by_id("samples/610-A", session)
    if sample:
        sample.delete(session)
    return sample


async def create_sample(request: Request):

    material_0 = Material(
        composition="composition1",
        mass=1.9
    )
    material_1 = Material(
        composition="composition1",
        mass=1.6
    )
    material_2 = Material(
        composition="composition2",
        mass=1.3
    )

    material_3 = Material(
        composition="composition3",
        mass=1.99
    )
    
    environment_data = Environment(
        description="description",
        ambiant_medium= material_3,
        temperature=33,
        pressure=2.7,
        relative_humidity=12.90

    )
    saved_environment_data = await environment_data.save(request.state.dbsession)

    
    layers = [
        Layer(
            material=material_1,
            thickness=0.99
        ), 
        Layer(
        material=material_2,
        thickness=0.2
        )
    ]
    substrate = Substrate(
        material=material_0,
        thickness=0.4,
        geometry="geo2"
    )
    
    #create sample data object
    print("saved_environment_data.Id", saved_environment_data.Id)
    sample = Sample(
        description="sample data",
        environment_ids= [saved_environment_data.Id],
        substrate=substrate,
        main_layer_index= 0,
        layers=layers
    )
    saved_sample = await sample.save(request.state.dbsession)
    return saved_sample