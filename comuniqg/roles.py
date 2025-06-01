from rolepermissions.roles import AbstractUserRole

module_servicos = "module_servicos"

class UsuarioMaster(AbstractUserRole):
    available_permissions = {
        module_servicos: True,
    }
