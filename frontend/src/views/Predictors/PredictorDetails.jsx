import {
    Button,
    IconButton,
    Stack,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
    Flex
  } from "@chakra-ui/react";
  import { useContext } from "react";
  import { useCompositeState } from "ds4biz-core";
  import { CLIENT, StateContext } from "../../config/constants";
  import { RiArrowLeftLine } from "react-icons/ri";
  import { useEffect, useState } from "react";

  
  export function PredictorDetails({ onClose, name }) {
    const state = useCompositeState({ blueprint: "Not Available" });

    const _state = useContext(StateContext);
    console.log("name::: ", {name})

    useEffect(() => {
        CLIENT.predictors[name]
        .get()
        .then((resp) => {state.blueprint=resp.data})
        .catch((err) => console.log(err));
      }, []);
    
    return (
      <Stack w="100%" h="100%" spacing="2rem" color='#A9A9A9'>
      <IconButton
            size="sm"
            w="30px"
            h="30px"
            borderRadius={"full"}
            bg='#222222'
            icon={<RiArrowLeftLine />}
            onClick={onClose}
          />
        <Flex w="100vw" h="100vh" p="2rem" color="#000000">

            {JSON.stringify(state.blueprint)}
        </Flex>

      </Stack>
    );
  }
  