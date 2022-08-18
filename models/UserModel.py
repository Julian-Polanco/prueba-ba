from flask import jsonify
from database.db import get_connection
from .entities.User import userJoin, UserEdit
from werkzeug.security import check_password_hash


class UserModel():

    @classmethod
    def get_user(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT id, fullname, email FROM public.user where id = %s """, (id,))
                result = cursor.fetchone()

                response = jsonify(
                    status=401, message='User not found'), 401
                if result != None:
                    response = UserEdit(
                        result[0], result[1], result[2]).to_JSON()

            connection.close()
            return response
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login_user(self, email, password):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT password, id, rol_id FROM public.user where email = %s """, (email,))
                result = cursor.fetchone()

                response = jsonify(
                    status=401, message='Login failed, credentials incorrect'), 401
                if result != None and check_password_hash(result[0], password):
                    response = jsonify(
                        status=200, message='Login success', id=result[1], rol=result[2]), 200

            connection.close()
            return response
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register_user(self, user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO public.user (fullname, document, email, password)
                    VALUES (%s, %s, %s, %s)""", (user.fullName, user.document, user.email, user.password))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_user(self, id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM public.user WHERE id = %s """,
                    (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_users_from_admin(self):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT u.id, u.fullname, u.document, u.email, r.name FROM public.user u
                    INNER JOIN public.rol r ON u.rol_id = r.id
                    WHERE u.rol_id = 1 """)
                result = cursor.fetchall()

            users = []
            for user in result:
                users.append(
                    userJoin(user[0], user[1], user[2], user[3], user[4]).to_JSON())

            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_all_users_from_superadmin(self):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT u.id, u.fullname, u.document, u.email, r.name FROM public.user u
                    INNER JOIN public.rol r ON u.rol_id = r.id """)
                result = cursor.fetchall()

            users = []
            for user in result:
                users.append(
                    userJoin(user[0], user[1], user[2], user[3], user[4]).to_JSON())
            connection.close()
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user(self, fullName, email, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """update public.user set fullname = %s, email = %s where id=%s """,
                    (fullName, email, id, ))
                affected_rows = cursor.rowcount
                connection.commit()
            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
