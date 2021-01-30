import logging
import asyncio
import grpc
import settings.all_cameras as camera_utils

import traffic_pb2
import traffic_pb2_grpc


class TrafficService(traffic_pb2_grpc.TrafficServiceServicer):

    async def GetCameras(
            self, request: traffic_pb2.CamerasRequest,
            context: grpc.aio.ServicerContext) -> traffic_pb2.CamerasReply:

        cams = camera_utils.get_all_cameras()
        cams = cams[cams.url.str.len() >0].copy()
        titles = cams.title
        image_urls = cams.image_url.fillna('')
        urls = cams.url.fillna('')
        cameras = [traffic_pb2.Camera(name=name, url=url,  image_preview=image)
                   for name, url, image in zip(titles, urls, image_urls)]
        # print(cameras)

        reply = traffic_pb2.CamerasReply()
        reply.cameras.extend(cameras)
        return reply


async def serve() -> None:
    server = grpc.aio.server()
    traffic_pb2_grpc.add_TrafficServiceServicer_to_server(TrafficService(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    coro = serve()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(coro)
    if False:
        asyncio.run(serve())
