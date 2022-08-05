from ds4biz_commons.business.factories import BaseFactory
from sktime.transformations.compose import TransformerPipeline
from ds4biz_commons.utils.submodules import ClassByNameLoader

FACTORY = BaseFactory()

for name,kl in ClassByNameLoader("sktime").klasses.items():
    FACTORY.register("skt."+name,list(kl)[0])
FACTORY.register("skt.TransformerPipeline", TransformerPipeline)


if __name__ == '__main__':

    a = {"__klass__": "skt.TransformerPipeline",
                "steps": [{"__klass__": "skt.Deseasonalizer", "model":"multiplicative","sp":12 }]}
    r = FACTORY(a)
    print(type(r))