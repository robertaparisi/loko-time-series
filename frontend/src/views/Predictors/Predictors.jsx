import { Button, Flex, HStack, Stack } from "@chakra-ui/react";
import { useCompositeState } from "ds4biz-core";
import { useContext } from "react";
import { CLIENT, StateContext } from "../../config/constants";
import { Predictor } from "./Predictor";
import { PredictorCreation } from "./PredictorCreation";
import { RiAddFill } from 'react-icons/ri';
import { PredictorDetails } from "./PredictorDetails";


export function Predictors({ predictors }) {
  const state = useCompositeState({ view: "list", name:null });
  const _state = useContext(StateContext);

  switch (state.view) {
    case "list":
      return (
        <Stack w="100%" h="100%" spacing="2rem">
          <HStack>
            <Button onClick={(e) => (state.view = "new")} leftIcon={<RiAddFill />}>New predictor</Button>
          </HStack>

          <Stack>
            {predictors.map((name) => (
              <Predictor
                onClick={(e) => {state.view = "show_blueprint", state.name ={name}}}
                name={name}
                key={name}
                onDelete={(e) =>
                  CLIENT.predictors[name].delete().then((resp) => {
                    _state.refresh = new Date();
                  })
                }
              />
            ))}
          </Stack>
        </Stack>
      );
    case "new":
      return (
        
        <Flex w="100vw" h="100vh" p="2rem">
          <PredictorCreation onClose={(e) => (state.view = "list")} />
        </Flex>
      );
    case "show_blueprint":
      console.log("PREDICTORS in detailssssssss::::")
      return (
        <Flex w="100vw" h="100vh" p="2rem">
          <PredictorDetails onClose={(e) => (state.view = "list")} name={Object.values(state.name)} />
        </Flex>

      );
    
    default:
      break;
  }
}
