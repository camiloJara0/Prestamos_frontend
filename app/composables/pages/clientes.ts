import type { Cliente } from '#shared/types/clientes'
import { UBadge, UButton, UDropdownMenu } from '#components'
import { h } from 'vue'

export function useClientesActions() {
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
      header: 'Cedula'
    },
    {
      accessorKey: 'direccion',
      header: 'Direccion'
    },
    {
      accessorKey: 'telefono',
      header: 'Telefono'
    },
    {
      accessorKey: 'estado',
      header: 'Estado',
      cell: ({ row }: { row: { getValue: (key: string) => string } }) => {
        const estado = row.getValue('estado')

        const color
          = estado === 'activo'
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
      cell: ({ row }: { row: { original: Cliente } }) =>
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
    }
  ]

  function getRowItems(row: { original: Cliente }) {
    const cliente = row.original

    return [
      {
        type: 'label' as const,
        label: 'Acciones'
      },
      {
        label: 'Editar',
        onSelect() {
          editarCliente(cliente)
        }
      },
      {
        type: 'separator' as const
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

  }

  const cerrarCliente = () => {

  }

  const editarCliente = async (_cliente: Cliente) => {

  }

  const eliminarCliente = async (_cliente: Cliente) => {

  }

  return {
    agregarCliente,
    cerrarCliente,
    editarCliente,
    eliminarCliente,
    columns
  }
}
