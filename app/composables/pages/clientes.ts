import { useClienteStore } from "~/stores/pages/clientes";
import type { Cliente } from "~/types/clientes";
import { UBadge, UButton, UDropdownMenu } from '#components'
import { h } from 'vue'

export function useClientesActions() {

  const store = useClienteStore()

  const columns = [
    {
        accessorKey: 'id',
        header: 'ID'
    },
    {
        accessorKey: 'nombre',
        header: 'Nombre'
    },
    {
        accessorKey: 'cedula',
        header: 'Cedula',
    },
    {
        accessorKey: 'direccion',
        header: 'Direccion',
    },
    {
        accessorKey: 'telefono',
        header: 'Telefono',
    },
    {
        accessorKey: 'estado',
        header: 'Estado',
        cell: ({ row }) => {
            const estado = row.getValue('estado')

            const color =
                estado === 'activo'
                ? 'success'
                : estado === 'inactivo'
                ? 'neutral'
                : 'warning'

            return h(
                UBadge,
                { variant: 'subtle', color, class: 'capitalize' },
                () => estado
            )
        }
    },
    {
        id: 'actions',
        cell: ({ row }) =>
        h(
            'div',
            { class: 'text-right' },
            h(
            UDropdownMenu,
            {
                content: { align: 'end' },
                items: getRowItems(row)
            },
            () =>
                h(UButton, {
                icon: 'i-lucide-ellipsis-vertical',
                color: 'neutral',
                variant: 'ghost'
                })
            )
        )
    },
  ]

function getRowItems(row) {
  const cliente = row.original

  return [
    {
      type: 'label',
      label: 'Acciones'
    },
    {
      label: 'Editar',
      onSelect() {
        editarCliente(cliente)
      }
    },
    {
      type: 'separator'
    },
    {
      label: 'Eliminar',
      onSelect() {
        eliminarCliente(cliente)
      }
    }
  ]
}
  
  const agregarCliente = () => {

  };

  const cerrarCliente = () => {

  };

  const editarCliente = async () => {

  };

  const eliminarCliente = async () => {

  };

  return {
    agregarCliente,
    cerrarCliente,
    editarCliente,
    eliminarCliente,
    columns
  };
}
