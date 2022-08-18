from multiprocessing import connection
from flask import jsonify
from database.db import get_connection
from .entities.Room import Room, RoomJoin
from .entities.Comment import CommentJoinUser


class RoomModel():

    @classmethod
    def register(self, room):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.room (name, description_short, description_large, price, code)
                    VALUES (%s, %s, %s, %s, %s)""", (room.name, room.descriptionShort, room.descriptionLarge, room.price, room.code,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_images(self, code, path_save_image, mimetype, file):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT id FROM public.room where code = %s """, (code,))
                result = cursor.fetchone()

                if result != None:
                    cursor.execute(
                        """INSERT INTO public.images_room (room_id, url, mimetype, file)
                    VALUES (%s, %s, %s, %s)""", (result[0], path_save_image, mimetype, file,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_names_images(self, code):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT url FROM public.room r
                    JOIN public.images_room ir ON r.id = ir.room_id
                    WHERE r.code = %s """, (code,))
                result = cursor.fetchall()

            connection.close()
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_ids_images(self, code):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT ir.id FROM public.room r
                    JOIN public.images_room ir ON r.id = ir.room_id
                    WHERE r.code = %s """, (code,))
                result = cursor.fetchall()

            connection.close()
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_file_image(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT file, mimetype FROM public.images_room ir
                    WHERE ir.id = %s """, (id,))
                result = cursor.fetchone()

            connection.close()
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_rooms(self):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT DISTINCT ON (name) name, description_short, description_large,
                    price, code, score, ir.id FROM public.room r JOIN public.images_room ir
                    ON ir.room_id = r.id """)
                result = cursor.fetchall()

            rooms = []
            for room in result:
                rooms.append(
                    RoomJoin(room[0], room[1], room[2], room[3], room[4], room[5], room[6]).to_JSON())

            connection.close()
            return rooms
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_rooms_between(self, startDate, endDate):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT r.name, r.description_short, r.description_large,
                    r.price, r.code, r.score FROM public.room r left JOIN public.reserve re
                    ON re.room_code = r.code 
                    WHERE
                    ( %s NOT BETWEEN re.start_date AND re.end_date)
                    OR
                    ( %s NOT BETWEEN re.start_date AND re.end_date) """, (startDate, endDate,))
                result = cursor.fetchall()
                if len(result) == 0:
                    cursor.execute(
                        """SELECT r.name, r.description_short, r.description_large,
                    r.price, r.code, r.score FROM public.room r """, (startDate, endDate,))
                result = cursor.fetchall()

            rooms = []
            for room in result:
                rooms.append(
                    Room(room[0], room[1], room[2], room[3], room[4], room[5]).to_JSON())

            connection.close()
            return rooms
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_room_detail(self, codeRoom):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT name, description_short, description_large,
                    price, code, score FROM public.room WHERE code = %s """, (codeRoom,))
                result = cursor.fetchone()

                room = Room(result[0], result[1], result[2],
                            result[3], result[4], result[5]).to_JSON()

            connection.close()
            return room
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_room(self, roomCode):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM public.room WHERE code = %s """,
                    (roomCode,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_room(self, name, descriptionShort, descriptionLarge, price, roomCode):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE public.room SET name = %s, description_short = %s,
                    description_large = %s, price = %s WHERE code=%s  """,
                    (name, descriptionShort, descriptionLarge, price, roomCode))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def can_add_comment(self, userId, codeRoom):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT r.id
                    FROM public.reserve r
                    WHERE r.user_id = %s AND r.room_code = %s
                    AND CURRENT_DATE > r.end_date """, (userId, codeRoom,))
                result = cursor.fetchall()

            connection.close()
            return result
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_room_comment(self, comment):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.comment (user_id, room_code, score, comment)
                    VALUES (%s, %s, %s, %s)""", (comment.userId, comment.roomCode, comment.score, comment.comment,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_room_comment(self, commentId):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM public.comment WHERE id=%s """,
                    (commentId,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_room_comments(self, codeRoom):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT c.id, user_id, room_code, score, comment, u.fullname
                    FROM public.comment c
                    JOIN public.user u ON u.id = c.user_id
                    WHERE room_code = %s """, (codeRoom,))

                result = cursor.fetchall()

                comments = []
                for comment in result:
                    comments.append(
                        CommentJoinUser(comment[0], comment[1], comment[2], comment[3], comment[4], comment[5]).to_JSON())

                connection.close()
                return comments
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def reserve(self, reserve):
        try:
            connection = get_connection()

            affected_rows = 0

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT room_code
                    FROM public.reserve r
                    WHERE
                    (%s BETWEEN r.start_date and r.start_date )
                    OR
                    (%s BETWEEN r.start_date and r.end_date ) """, (reserve.startDate, reserve.endDate,))
                result = cursor.fetchone()

                if result == None:
                    cursor.execute(
                        """INSERT INTO public.reserve (user_id, room_code, start_date, end_date)
                        VALUES (%s, %s, %s, %s)""", (reserve.userId, reserve.roomCode, reserve.startDate, reserve.endDate,))
                    affected_rows = cursor.rowcount
                    connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
