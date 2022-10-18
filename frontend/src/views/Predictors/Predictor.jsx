import { Box, Button, HStack, IconButton, Spacer, Stack, Tag, Flex, Text } from "@chakra-ui/react";
import { RiDeleteBin4Line, RiFolderDownloadLine } from "react-icons/ri";
import { useCompositeState } from "ds4biz-core";
import { useEffect, useState } from "react";
import { CLIENT, baseURL} from "../../config/constants";
import urlJoin from 'url-join';
import { PredictorDetails } from "./PredictorDetails";



export function Predictor({ name, onClick, onDelete, onExport, ...rest }) {

  const state = useCompositeState({
    model: null,
    transformer: null,
    view: "general",
    model_type: "Auto",
    transformer_type: "Auto",
    status_tag: null
  });
  


  useEffect(() => {
    CLIENT.predictors[name]
    .get()
    .then((resp) => {state.model=resp.data.steps.model
                      state.transformer = resp.data.steps.transformer
                      state.model_type = resp.data.steps.model.__klass__.split(".").at(-1)
                      state.transformer_type = resp.data.steps.transformer.__klass__.split(".").at(-1)                      
                      state.status_tag = resp.data.status ??= "Not Fitted"
                    })
    .catch((err) => console.log(err));
  }, []);

  // console.log("MODELLLLL",state.model)
  console.log("PRED NAME ::", name)
  console.log("Status TAG ::",state.status_tag)

  let color_status = "#fcec85"
  if (state.status_tag=="Fitted") {
    color_status = "#94c099";
  } else if (state.status_tag=="Training") {
    color_status = "#df8e6e";
    //#d06464
  } 



  switch (state.view){
  case "details":
    console.log("in detailssssssss::::")
      return (
        <Flex w="100vw" h="100vh" p="2rem">
          <PredictorDetails onClose={(e) => (state.view = "general")} name={name} />
        </Flex>

      );
  case "general":
      return (
      // <a href={urlJoin(baseURL, 'predictors', name)} target="_blank">
    
      // <Button onClick={(e) => (state.view="details")}>
      <HStack
        bg="gray.200"
        borderRadius={"10px"}
        w="100%"
        py="0.5rem"
        px="1rem"
        onClick={(e)=> onClick(e)}
        {...rest} 
      >
        <Stack spacing={0}>
          <HStack color={"pink.500"}>
            <Box><Text as="b" color='#3f986c'>{name}</Text></Box>
            <Tag borderRadius={"10px"} p=".3rem" bg={color_status} fontSize="xs">
              {state.status_tag}
            </Tag>
          </HStack>
          <HStack fontSize={"xs"}>
            <Stack spacing="0">
              <Box><Text as="b">Model</Text></Box>
              <Box>{state.model_type}</Box>
            </Stack>
            <Stack spacing="0">
              <Box><Text as="b">Transformer</Text></Box>
              <Box>{state.transformer_type}</Box>
            </Stack>
          </HStack>
        </Stack>
        <Spacer />
        <HStack>
          <IconButton
            size="sm"
            borderRadius={"full"}
            icon={<RiDeleteBin4Line />}
            onClick={(e) => {
              e.stopPropagation();
              e.preventDefault();
              onDelete(e);
            }}
          />
        <IconButton
          size="sm"
          borderRadius={"full"}
          icon={<RiFolderDownloadLine />}
          onClick={(e) => {
            e.stopPropagation();
            e.preventDefault();
            onExport(e);
          }}
        />
        </HStack>
      </HStack>
    
  // </Button> 
  );
  }
}
